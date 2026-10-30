import re

from PIL import Image
from playwright.sync_api import expect

from properties.models import Property


def make_photo(tmp_path):
    path = tmp_path / 'photo.png'
    Image.new('RGB', (400, 300), 'skyblue').save(path)
    return str(path)


def test_login_shows_username(page, live_server, owner, login):
    login('owner')
    expect(page.locator('.site-header')).to_contain_text('owner')
    expect(page.locator('.site-header')).not_to_contain_text('Увійти')


def test_login_with_wrong_password_fails(page, live_server, owner, login):
    login('owner', 'wrong-password')
    expect(page).to_have_url(f'{live_server.url}/login/')
    expect(page.locator('.site-header')).to_contain_text('Увійти')


def test_logout(page, live_server, owner, login):
    login('owner')
    page.click('.site-header .dropdown-toggle')
    page.click('text=Вийти')
    expect(page.locator('.site-header')).to_contain_text('Увійти')


def test_anonymous_is_sent_to_login_when_creating(page, live_server, transactional_db):
    page.goto(f'{live_server.url}/property/create/')
    expect(page).to_have_url(f'{live_server.url}/login/?next=/property/create/')


def test_create_property(page, live_server, owner, category, login, tmp_path):
    login('owner')
    page.goto(f'{live_server.url}/property/create/')
    page.fill('input[name="title"]', 'Будинок біля лісу')
    page.fill('input[name="price"]', '250000')
    page.select_option('select[name="deal_type"]', 'sale')
    page.fill('input[name="area_sqm"]', '120')
    page.fill('input[name="rooms"]', '4')
    page.fill('input[name="address"]', 'Київ, Пуща-Водиця')
    page.set_input_files('#id_main_image', make_photo(tmp_path))
    expect(page.locator('#main-info')).to_contain_text('400×300')
    page.select_option('select[name="category"]', str(category.pk))
    page.get_by_role('button', name='Зберегти').click()

    expect(page.locator('h1')).to_have_text('Будинок біля лісу')
    assert Property.objects.get(title='Будинок біля лісу').owner == owner


def test_owner_edits_price(page, live_server, flat, login, tmp_path):
    login('owner')
    page.goto(f'{live_server.url}/property/{flat.pk}/')
    page.get_by_role('link', name='Редагувати').click()
    page.fill('input[name="price"]', '99000')
    page.set_input_files('#id_main_image', make_photo(tmp_path))
    page.get_by_role('button', name='Зберегти').click()

    expect(page.locator('.contact-card .price')).to_contain_text('99')
    flat.refresh_from_db()
    assert flat.price == 99000


def test_owner_deletes_property(page, live_server, flat, login):
    login('owner')
    page.goto(f'{live_server.url}/property/{flat.pk}/')
    page.get_by_role('link', name='Видалити').click()
    page.get_by_role('button', name='Так, видалити').click()

    expect(page).to_have_url(f'{live_server.url}/properties/')
    expect(page.locator('body')).not_to_contain_text('Квартира на Печерську')
    assert not Property.objects.filter(pk=flat.pk).exists()


def test_stranger_does_not_see_edit_buttons(page, live_server, flat, stranger, login):
    login('stranger')
    page.goto(f'{live_server.url}/property/{flat.pk}/')
    expect(page.locator('h1')).to_have_text('Квартира на Печерську')
    expect(page.get_by_role('link', name='Редагувати')).to_have_count(0)
    expect(page.get_by_role('link', name='Видалити')).to_have_count(0)


def test_catalog_filter_by_rent(page, live_server, flat, owner, category):
    Property.objects.create(
        title='Студія в оренду', price=500, deal_type='rent', area_sqm=25, rooms=1,
        address='Львів', owner=owner, category=category,
    )
    page.goto(f'{live_server.url}/properties/')
    expect(page.locator('.property-card')).to_have_count(2)

    page.select_option('select[name="deal_type"]', 'rent')
    page.get_by_role('button', name='Застосувати').click()

    expect(page.locator('.property-card')).to_have_count(1)
    expect(page.locator('.property-card')).to_contain_text('Студія в оренду')


def test_property_page_has_seo_title_and_contacts(page, live_server, flat):
    page.goto(f'{live_server.url}/property/{flat.pk}/')
    expect(page).to_have_title(re.compile(r'Квартира на Печерську — Продаж, \$150\s000 \| DomHub'))
    expect(page.locator('meta[name="description"]')).to_have_attribute('content', re.compile('Київ, Печерськ'))
    expect(page.locator('.contact-card')).to_be_visible()
    expect(page.locator('.contact-card .price')).to_contain_text('150')


def test_map_shows_objects_and_filters(page, live_server, flat, owner, category):
    Property.objects.create(
        title='Квартира у Львові', price=90000, deal_type='rent', area_sqm=50, rooms=2,
        address='Львів, центр', latitude=49.84, longitude=24.03, owner=owner, category=category,
    )
    page.goto(f'{live_server.url}/map/')
    expect(page.locator('#result-count')).to_have_text("Знайдено об'єктів: 2")
    expect(page.locator('.map-card')).to_have_count(2)

    page.locator('#deal-buttons [data-deal="rent"]').click()
    expect(page.locator('#result-count')).to_have_text("Знайдено об'єктів: 1")
    expect(page.locator('.map-card')).to_contain_text('Квартира у Львові')

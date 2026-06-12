# -*- coding: utf-8 -*-
"""End-to-end test of the demo ticket checkout with Playwright."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "_cmp", "cur")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 960})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto("http://127.0.0.1:8487/vstupenky.html")
    page.wait_for_timeout(3000)

    # STEP 1: pick tickets (2 adults, 1 child, 1 tour)
    page.click('.counter[data-type="adult"] .plus')
    page.click('.counter[data-type="adult"] .plus')
    page.click('.counter[data-type="child"] .plus')
    page.click('.counter[data-type="tour"] .plus')
    total = page.text_content("#sumTotal").strip()
    print("step1 total:", total)
    assert "800" in total, "expected 800 Kc total"
    page.screenshot(path=os.path.join(OUT, "co-step1.png"))

    # validation: removing adults must block
    page.click('.counter[data-type="adult"] .minus')
    page.click('.counter[data-type="adult"] .minus')
    page.click("#btnNext")
    page.wait_for_timeout(300)
    assert page.is_visible("#err1"), "expected validation error without adult"
    print("step1 validation OK:", page.text_content("#err1")[:60])
    page.click('.counter[data-type="adult"] .plus')
    page.click('.counter[data-type="adult"] .plus')
    page.click("#btnNext")
    page.wait_for_timeout(700)
    assert page.is_visible("#step2"), "step2 should be visible"

    # STEP 2: contact with bad email first
    page.fill("#fullName", "Jana Nováková")
    page.fill("#email", "spatny-email")
    page.click("#btnNext")
    page.wait_for_timeout(300)
    assert page.is_visible("#err2"), "expected email validation error"
    print("step2 validation OK")
    page.fill("#email", "jana.novakova@email.cz")
    page.fill("#phone", "+420 777 123 456")
    page.click("#btnNext")
    page.wait_for_timeout(700)
    assert page.is_visible("#step3"), "step3 should be visible"
    page.screenshot(path=os.path.join(OUT, "co-step3.png"))

    # QR payba tab renders a QR
    page.click('.pay-tab[data-pay="qr"]')
    page.wait_for_timeout(400)
    assert page.locator("#qrPay img, #qrPay canvas").count() > 0, "QR platba code should render"
    print("QR platba renders OK")
    page.screenshot(path=os.path.join(OUT, "co-qr.png"))

    # back to card, invalid card first
    page.click('.pay-tab[data-pay="card"]')
    page.fill("#ccNum", "1234")
    page.click("#btnNext")
    page.wait_for_timeout(300)
    assert page.is_visible("#err3"), "expected card validation error"
    print("card validation OK")

    # valid demo card
    page.fill("#ccNum", "4242424242424242")
    page.fill("#ccExp", "0830")
    page.fill("#ccCvc", "123")
    page.click("#btnNext")
    page.wait_for_timeout(2600)
    assert page.is_visible("#step4"), "step4 should be visible after payment"
    order = page.text_content("#orderCode").strip()
    tickets = page.locator("#ticketsList .eticket").count()
    qrs = page.evaluate(
        "() => [...document.querySelectorAll('#ticketsList .qr-target')].filter(t => t.querySelector('img,canvas')).length"
    )
    print("order:", order, "| tickets:", tickets, "| tickets with QR:", qrs)
    assert tickets == 4, "expected 4 e-tickets (2 adult + 1 child + 1 tour)"
    assert qrs == 4, "expected QR on every ticket"
    page.screenshot(path=os.path.join(OUT, "co-success.png"))

    # localStorage persisted
    saved = page.evaluate("() => !!localStorage.getItem('zs-demo-order')")
    print("localStorage saved:", saved)

    print("page errors:", errors if errors else "none")
    b.close()

from PIL import Image
for n in ["co-step1", "co-step3", "co-qr", "co-success"]:
    pth = os.path.join(OUT, n + ".png")
    img = Image.open(pth); img.thumbnail((640, 9999)); img.save(pth)
print("ALL CHECKS PASSED")

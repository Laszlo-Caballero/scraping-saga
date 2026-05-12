import asyncio
from playwright.async_api import async_playwright
import os
from enum_saga.saga_keys import DetailsKeys
from utils.utils import Utils
from model.product import Product
import json

path_json = "data/products.json"

saga_not_found = "https://www.falabella.com.pe/falabella-pe/notFound"

utils = Utils()


async def detalle():
    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        products_data = [Product(**item) for item in data]
        
    
    print(len(products_data))
    
    async with async_playwright() as p:
        context = await p.chromium.launch(headless=True)
        page = await context.new_page()
        
        aux = 0

        for product in products_data:
            try:
                aux += 1
                print(f"Procesando producto {aux}/{len(products_data)}: {product.name}")
                
                await page.goto(product.url)
                
                if page.url == saga_not_found:
                    print(f"Producto no encontrado: {product.name}")
                    continue
                
                await page.wait_for_selector(f"#{DetailsKeys.DETAIL_ID.value}")
                
            
                container = page.locator(f"#{DetailsKeys.DETAIL_ID.value}")
            
                
                breadcrumb_container = container.locator(f"div[{DetailsKeys.BREADCRUMB_CONTAINER_ID.value}]")    
                
                breadcrumbs = await breadcrumb_container.locator("li").all()
                
                category = await utils.error_wrapper(lambda: breadcrumbs[-2].locator("a").inner_text())
                
                product.set_category(category)
                
                sub_category = await utils.error_wrapper(lambda: breadcrumbs[-1].locator("a").inner_text())
                
                product.set_sub_category(sub_category)
                
                
                seller = await utils.error_wrapper(lambda: container.locator(f"#{DetailsKeys.SELLER_ID.value}").inner_text())
                
                product.set_seller(seller)
                
                spects_container = container.locator(f"div[{DetailsKeys.SPECTS_CONTAINER_ID.value}]")
                
                spects_items = await spects_container.locator("li").all()
                
                spects = []
                
                for item in spects_items:
                    spects_spans = await item.locator("span").all()
                    spect = ""
                    for span in spects_spans:
                        text = await span.inner_text()
                        spect += text + " "
                    spects.append(spect.strip())
                
                product.set_spects_raw(spects)
                
                
                caracterisitcs_accordeon = container.locator(f"#{DetailsKeys.SPECTS_ACCORDEON_ID.value}")
                
                buttons_caracteristics = await caracterisitcs_accordeon.locator("button").all()
                
                caracteriscts_container = None
                
                for button in buttons_caracteristics:
                    text = await button.inner_text()
                    
                    show_more_button = button.locator(f"button.{DetailsKeys.SHOW_MORE_SPECTS_BUTTON_CLASS.value}")
                    
                    if await show_more_button.count() > 0:
                        await show_more_button.click()
                    
                    if "Especificaciones" in text:
                        await button.click()
                        caracteriscts_container = container.locator(f"table.{DetailsKeys.SPECTS_CLASS_TABLE.value}")
                        break
                
                caracteristics = []
                
                if caracteriscts_container:
                    rows = await caracteriscts_container.locator("tr").all()
                    
                    for row in rows:
                        spans = await row.locator("td").all()
                        spect = ""
                        for span in spans:
                            text = await span.inner_text()
                            spect += text + " "
                        caracteristics.append(spect.strip())
                product.set_catarecteristics(caracteristics)      
                
                galery_container = container.locator(f"div.{DetailsKeys.GALERY_CONTAINER_CLASS.value}")
                
                galery_images = await galery_container.locator("img").all()
                
                two_first_images = galery_images[:2]
                
                images = []
                
                for img in two_first_images:
                    slug_name = utils.to_slug(product.name)
                    
                    error, img_url = await utils.error_wrapper(lambda: img.get_attribute("src"))
                    
                    print("URL de la imagen:", img_url)
                    
                    
                    if img_url:
                        new_img = img_url.replace("w=100,h=100", "w=1200,h=1200")
                        
                        destiny = f"{slug_name}"
                        name = f"{slug_name}_{len(images)+1}"
                        await utils.download_image(new_img, name, destiny)
                        images.append(f"data/images/{destiny}/{name}.webp")
                
                product.set_images(images)
            
            except Exception as e:
                print(f"Error procesando el producto {product.name}: {e}")
                product.set_error(str(e))
                    
                  
        
    with open("data/products_detailed.json", "w", encoding="utf-8") as f:
        json_data = [product.to_dict() for product in products_data]
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        


if __name__ == "__main__":
    asyncio.run(detalle())
import asyncio
from playwright.async_api import async_playwright
import os
from enum_saga.saga_keys import SagaKeys
from utils.utils import Utils
from model.product import Product
from repository.ProductRepository import ProductRepository
from detalle import detalle

# page_link = "https://www.falabella.com.pe/falabella-pe/collection/descuentos-cmr?sid=HO_X1___OUS_6940"
links = ["https://www.falabella.com.pe/falabella-pe/category/cat760702/Telefonia", 
         "https://www.falabella.com.pe/falabella-pe/category/cat50678/Computadoras",
         "https://www.falabella.com.pe/falabella-pe/category/cat40488/Audio",
         "https://www.falabella.com.pe/falabella-pe/category/cat210477/TV-Televisores"]

utils = Utils()
product_repository = ProductRepository()


async def scraping(page_link: str):
    os.makedirs("data/images", exist_ok=True)
    
    async with async_playwright() as p:
        context = await p.chromium.launch(headless=True)
        page = await context.new_page()
        
        await page.goto(page_link)
        
        await page.wait_for_selector(f"#{SagaKeys.PRODUCTS_ID.value}")
        
        actual_page = 1
        
        is_last_page = False
        
        total_page_container = page.locator(f"#{SagaKeys.TOTAL_PAGES_CONTAINER_ID.value}")
        
        buttons = await total_page_container.locator("button").all()
        
        last_page_button = buttons[-2]
        
        total_pages = int(await last_page_button.locator("p").inner_text())
        
        print("Total de páginas:", total_pages)
                

        while not is_last_page:
            
            link = ""
            if actual_page > 1:
                link = f"{page_link}?page={actual_page}"
                await page.goto(link)
            
            container = page.locator(f"#{SagaKeys.PRODUCTS_ID.value}")
            print(f"Página {actual_page}")
            
            await page.wait_for_selector(f"div.{SagaKeys.LOADER_CLASS.value}", state="detached")
            all_products = await container.locator(f"div[{SagaKeys.PRODUCT_SELECTOR.value}]").all()
            
            if len(all_products) == 0:
                print("No se encontraron productos.")
                break
            
            
            for idx, product in enumerate(all_products):
                print(f"Procesando producto {idx + 1} de {len(all_products)}")
                product_append = Product()

                try:
                    url = await utils.error_wrapper(lambda: product.locator("a").get_attribute("href"))
                    product_append.set_url(url)
                    brand = await utils.error_wrapper(lambda: product.locator(f"b.{SagaKeys.BRAND_CLASS.value}").inner_text()) 
                    product_append.set_brand(brand)

                    name = await utils.error_wrapper(lambda: product.locator(f"b.{SagaKeys.NAME_CLASS.value}").inner_text())
                    product_append.set_name(name)

                    prices_container = product.locator(f"ol.{SagaKeys.PRICES_CONTAINER_CLASS.value}")
                    
                    prices = []
                    
                    for price in await prices_container.locator("li").all():
                        first_span = price.locator("span").first
                        price = await utils.error_wrapper(lambda: first_span.inner_text())
                        prices.append(price)
                    product_append.set_price(prices)

                    

                except Exception as e:
                    print(f"Error al procesar el producto: {str(e)}")
                    product_append.set_error(str(e))
                    continue
                finally:
                    await product_repository.insert_product(product_append)
        
            if actual_page == total_pages:
                is_last_page = True
            else: 
                actual_page += 1
        




async def main():
    await product_repository.create_table()
    for link in links:
        await scraping(link)

    await detalle()
    
    print("Proceso de scraping y detalle completado.")


if __name__ == "__main__":
    asyncio.run(main())
from typing import Optional

from utils.custom_client import Client


class BillzService:
    def __init__(self):
        self.client = Client()
    
    async def set_user(
        self,
        chat_id: str,
        first_name: str, 
        last_name: str, 
        phone_number: str, 
        date_of_birth: Optional[str] = '2022-05-14',
        gender: Optional[int] = 1,
    ):
        url = 'https://api-admin.billz.ai/v1/client'
        payload = {
            "chat_id": chat_id,
            "date_of_birth": date_of_birth,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "gender": gender
        }

        async with self.client as client:
            await client.post(url, payload)

    async def get_products(self, limit: int, page: int, search: str = None):
        """
        TODO: 
        1. All products with parent_id
        2. All products with main_image_url_full
        3. All products with product_supplier_stock[0].wholesale_price
        4. All products with shop_measurement_values[0].active_measurement_value
        """
        url = f'https://api-admin.billz.ai/v2/products?limit=4000&page=1' 
        url += f'&search={search}' if search else ''


        
        async with self.client as client:
            data = await client.get(url)
            products = []
            for obj in data['products']:
                if (
                    obj['parent_id'] and obj['main_image_url_full'] and 
                    obj['product_supplier_stock'] and 
                    obj['product_supplier_stock'][0]['wholesale_price'] and 
                    obj['shop_measurement_values'] and
                    obj['shop_measurement_values'][0]['active_measurement_value']
                ):
                    products.append(obj)
            
            page, limit = (page - 1) * limit, (limit * page)

            print("page:", page)
            print("limit:", limit)
            print("product len:", len(products[page:limit]))

            result = {}
            result["count"] = len(products)
            result["products"] = products[page:limit]

            return result if result else result

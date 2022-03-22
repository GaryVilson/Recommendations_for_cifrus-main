from main.models import Category, Subcategory, Products


def list_to_dict(lst: list) -> dict:
    dictionary = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return dictionary


def run(product: Products) -> list[Products]:
    product_specs = list_to_dict(product.specifications)
    products = Products.objects.filter(category=product.category).exclude(subcategory=product.subcategory)
    recommended_products = dict()
    for recommended_product in products:
        similarities = 0
        recommended_product_specs = list_to_dict(recommended_product.specifications)
        for spec in product_specs.keys():
            if spec in recommended_product_specs.keys() and product_specs[spec] == recommended_product_specs[spec]:
                similarities += 1
        recommended_products[recommended_product.id] = similarities
    recommended_products = sorted(recommended_products.items(), key=lambda x: int(x[1]), reverse=True)[:6]
    return [product[0] for product in recommended_products]


if __name__ == '__main__':
    run()

---
id: DOMAIN_TO_EXTERNAL_LANGUAGE
title: "Domain-to-External uses domain language."
essence: "The translator speaks domain language on one side and external format on the other, so neither leaks into the other."
---

When translating domain objects to external formats, use domain concepts in the translator. Don't leak external concerns into the domain.

```python
# Domain → External API
def domain_to_api_translator(
    order: Order
) -> tuple[TranslatorError | None, OrderApiDict | None]:
    try:
        return None, {
            "orderId": str(order.id),
            "customerEmail": order.customer.email,
            "items": [
                {
                    "sku": item.product.sku,
                    "quantity": item.quantity,
                    "priceInCents": int(item.price * 100)
                }
                for item in order.items
            ],
            "totalInCents": int(order.total * 100)
        }
    except AttributeError as e:
        return TranslatorError(f"Missing required attribute: {e}"), None
```
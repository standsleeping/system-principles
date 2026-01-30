---
id: CROSS_DOMAIN_ENFORCE_RULES
title: "Cross-domain translators enforce boundary rules."
summary: "When translating between domain contexts, enforce the boundary's invariants. This is still structural validation, not business logic."
---

When translating between domain contexts, enforce the boundary's invariants. This is still structural validation, not business logic.

```python
# Billing context → Shipping context
def billing_to_shipping_translator(
    billing_order: BillingOrder
) -> tuple[TranslatorError | None, ShippingRequest | None]:
    # Structural requirement: shipping needs paid orders
    if billing_order.status != "PAID":
        return TranslatorError("Order must be paid before shipping"), None

    return None, ShippingRequest(
        order_ref=billing_order.id,
        recipient=Address(
            name=billing_order.customer_name,
            street=billing_order.delivery_address,
            postal_code=billing_order.postal_code
        ),
        items=[
            ShippingItem(sku=item.sku, quantity=item.qty)
            for item in billing_order.line_items
        ]
    )
```
from customer.models import Customer

def customer_context(request):
    """
    Makes the `customer` object available globally in templates
    if the user is logged in and has a valid session.
    """
    customer_id = request.session.get('customer_id')
    if customer_id:
        try:
            customer = Customer.objects.get(user_id=customer_id)
            return {'customer': customer}
        except Customer.DoesNotExist:
            pass
    return {'customer': None}

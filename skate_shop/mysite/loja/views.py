from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # type: ignore # Import messages for user feedback
from .forms import CustomLoginForm, CustomSignUpForm  # type: ignore # Import both forms
from .models import Product, Cart, CartItem

# Existing lista_produtos view
def lista_produtos(request):
    # Dummy data or fetch from the database
    produtos = [
        {'name': 'Skateboard', 'price': 100},
        {'name': 'Skate Shoes', 'price': 50},
        {'name': 'Helmet', 'price': 30},
    ]
    return render(request, 'loja/lista_produtos.html', {'produtos': produtos})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)  # Only pass POST data here
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_produtos')  # Redirect to product list
            else:
                form.add_error(None, 'Invalid username or password.')  # Optional: Add error if authentication fails
    else:
        form = CustomLoginForm()  # Initialize an empty form for GET requests

    return render(request, 'loja/login.html', {'form': form})

# User signup view
def user_signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            return _extracted_from_user_signup_5(form, request)
    else:
        form = CustomSignUpForm()  # Display the form
    return render(request, 'loja/signup.html', {'form': form})  # Render signup template

# Function to handle user signup logic
def _extracted_from_user_signup_5(form, request):
    form.save()  # Create the user
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=password)
    login(request, user)  # Log the user in
    return redirect('lista_produtos')  # Redirect to product list

# User logout view
def user_logout(request):
    logout(request)
    return redirect('lista_produtos')

# Add to cart view
def add_to_cart(request, product_id):
    print(f"Adding product with ID: {product_id}")  # Debug log
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)  # Ensure the product exists
        
        cart, created = Cart.objects.get_or_create(user=request.user)  # Get or create the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  # Get or create the cart item

        if not created:  # If the item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"Updated quantity of {product.name} in cart.")
        else:
            messages.success(request, f"{product.name} added to cart.")

        return redirect('lista_produtos')  # Redirect back to the product list

    messages.warning(request, "You need to log in to add items to the cart.")
    return redirect('user_login')  # Redirect to login if user is not authenticated

# View cart function
def view_cart(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)  # Fetch cart safely
        cart_items = CartItem.objects.filter(cart=cart)  # Get all items in the cart
        grand_total = sum(item.product.price * item.quantity for item in cart_items)  # Calculate grand total
        return render(request, 'loja/cart.html', {'cart_items': cart_items, 'grand_total': grand_total})
    return redirect('user_login')    # Redirect to login if user is not authenticated

# loja/views.py

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)  # Fetch cart item
        if cart_item.cart.user == request.user:  # Check ownership
            cart_item.delete()  # Remove the item
    return redirect('view_cart')  # Redirect to the cart view


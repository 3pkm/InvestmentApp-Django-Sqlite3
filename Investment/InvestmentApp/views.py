from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from decimal import Decimal

from .models import Product, Investment

@login_required
def index(request):
    total_customers = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
    total_investment = Investment.objects.aggregate(total=Sum('investment_amount'))['total'] or 0

    investments = Investment.objects.select_related('customer', 'product').all()
    users = User.objects.filter(is_staff=False)
    products = Product.objects.all()  # Ensure products are fetched

    return render(request, 'Investment/index.html', {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_investment': total_investment,
        'investments': investments,
        'customers': users,
        'products': products,  # Pass products to the template
    })
    
@login_required
def add_investment(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        investment_amount = request.POST.get('investment_amount')

        # Validate investment amount
        try:
            amount = float(investment_amount)
            if amount <= 0:
                return JsonResponse({'success': False, 'error': 'Investment amount must be positive.'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid investment amount.'}, status=400)

        try:
            customer = User.objects.get(id=customer_id)  # Ensure the user exists
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Customer does not exist.'}, status=400)

        try:
            product = Product.objects.get(id=product_id)  # Ensure the product exists
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product does not exist.'}, status=400)

        # Create the investment
        try:
            Investment.objects.create(
                customer=customer,
                product=product,
                investment_amount=investment_amount
            )
            return JsonResponse({'success': True, 'message': 'Investment added successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

@login_required
def delete_investment(request, investment_id):
    if request.method == 'POST':
        try:
            investment = get_object_or_404(Investment, id=investment_id)
            investment.delete()
            return JsonResponse({'success': True, 'message': 'Investment deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def update_investment(request, investment_id):
    if request.method == 'POST':
        try:
            investment = get_object_or_404(Investment, id=investment_id)
            investment_amount = request.POST.get('investment_amount')

            if not investment_amount or float(investment_amount) <= 0:
                return JsonResponse({'success': False, 'error': 'Invalid investment amount'}, status=400)

            investment.investment_amount = investment_amount
            investment.save()
            return JsonResponse({'success': True, 'message': 'Investment updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('home')
        else:
            # If the form is invalid, pass the errors back to the template
            return render(request, 'Investment/register.html', {'form': form})
    else:
        form = UserCreationForm()

    return render(request, 'Investment/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Investment/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'Investment/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def products_view(request):
    products = Product.objects.all()
    return render(request, 'Investment/products.html', {'products': products})

@login_required
def investments_view(request):
    investments = Investment.objects.select_related('customer', 'product').all()
    return render(request, 'Investment/investments.html', {'investments': investments})

@login_required
def monthly_investment_calculator(request):
    customers = User.objects.filter(is_staff=False)

    if request.method == "POST":
        customer_id = request.POST.get('customer')
        try:
            time_duration_years = Decimal(request.POST.get('time_duration', 0))  
            expected_return_rate = Decimal(request.POST.get('expected_return_rate', 0))
            monthly_investment = Decimal(request.POST.get('monthly_investment', 0))

            
            customer = User.objects.get(id=customer_id)
            existing_investments = Investment.objects.filter(customer=customer).aggregate(
                Sum('investment_amount')
            )['investment_amount__sum'] or Decimal(0)

            # Calculations
            r = expected_return_rate / Decimal(12 * 100)  # Monthly interest rate
            n = time_duration_years * Decimal(12)  # Total months
            total_invested = monthly_investment * n  # Total amount invested

            if r > 0:
                maturity_amount = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)
            else:
                maturity_amount = total_invested  # No interest scenario

            total_with_existing = existing_investments + maturity_amount  # Add existing investments to future value

            return render(request, 'Investment/monthly_calculator.html', {
                'customers': customers,
                'result': round(maturity_amount, 2),
                'total_invested': round(total_invested, 2),
                'existing_investments': round(existing_investments, 2),
                'total_with_existing': round(total_with_existing, 2),
                'monthly_investment': monthly_investment,
                'time_duration_years': time_duration_years,
                'expected_return_rate': expected_return_rate,
            })
        except (ValueError, Decimal.InvalidOperation):
            return render(request, 'Investment/monthly_calculator.html', {
                'customers': customers,
                'error': 'Invalid input. Please enter valid numbers.',
            })
            
    return render(request, 'Investment/monthly_calculator.html', {'customers': customers})

@login_required
def one_time_investment_calculator(request):
    customers = User.objects.filter(is_staff=False)

    if request.method == "POST":
        customer_id = request.POST.get('customer')
        try:
            # Parse inputs
            time_duration_years = Decimal(request.POST.get('time_duration', 0))  # Duration in years
            expected_return_rate = Decimal(request.POST.get('expected_return_rate', 0))  # Annual rate in %
            compounding_frequency = Decimal(12)  # Compounding monthly
            one_time_investment = Decimal(request.POST.get('one_time_investment', 0) or 0)  # Handle empty field

            # Retrieve customer investments
            customer = User.objects.get(id=customer_id)
            existing_investments = Investment.objects.filter(customer=customer).aggregate(
                Sum('investment_amount')
            )['investment_amount__sum'] or Decimal(0)
            
            # Total investment is existing plus any additional one-time investment
            total_investment = existing_investments + one_time_investment

            # Calculations
            r = expected_return_rate / Decimal(100)  # Annual rate in decimal
            n = compounding_frequency
            t = time_duration_years

            estimated_return = total_investment * (1 + (r / n)) ** (n * t)

            return render(request, 'Investment/one_time_calculator.html', {
                'customers': customers,
                'result': round(estimated_return, 2),
                'total_investment': round(total_investment, 2),
                'existing_investments': round(existing_investments, 2),
                'one_time_investment': round(one_time_investment, 2),
                'time_duration_years': time_duration_years,
                'expected_return_rate': expected_return_rate,
            })
        except (ValueError, Decimal.InvalidOperation):
            return render(request, 'Investment/one_time_calculator.html', {
                'customers': customers,
                'error': 'Invalid input. Please enter valid numbers.',
            })

    return render(request, 'Investment/one_time_calculator.html', {'customers': customers})

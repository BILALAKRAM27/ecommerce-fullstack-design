from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Buyer
from .forms import BuyerUpdateForm


# Create your views here.
@login_required
def buyer_profile_view(request):
    try:
        buyer = Buyer.objects.get(email=request.user.email)
        context = {
            'buyer': buyer,
            'image_base64': buyer.get_image_base64()
        }
        return render(request, 'buyer/buyer_profile.html', context)
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer profile not found.')
        return redirect('sellers:login')


# UPDATE Buyer
@login_required
def update_buyer_view(request):
    try:
        buyer = Buyer.objects.get(email=request.user.email)
        if request.method == 'POST':
            form = BuyerUpdateForm(request.POST, request.FILES, instance=buyer)
            if form.is_valid():
                buyer = form.save()
                messages.success(request, 'Buyer profile updated successfully.')
                return redirect('buyer:buyer_profile')
        else:
            form = BuyerUpdateForm(instance=buyer)
        return render(request, 'buyer/buyer_update.html', {'form': form})
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer profile not found.')
        return redirect('sellers:login')


# DELETE Buyer
@login_required
def delete_buyer_view(request):
    try:
        buyer = Buyer.objects.get(email=request.user.email)
        if request.method == 'POST':
            # Delete the buyer profile
            buyer.delete()
            messages.success(request, 'Your buyer account has been deleted.')
            return redirect('sellers:login')
        return render(request, 'buyer/buyer_delete.html')
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer profile not found.')
        return redirect('sellers:login')
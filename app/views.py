# Django imports
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic import TemplateView

# StatelyDB client functions
from .stately_client import (
    get_profile_and_links,
    get_link_by_id,
    increment_profile_views,
    increment_link_clicks,
    create_link,
    delete_link,
    rename_profile,
    update_profile_bio,
    create_profile
)
import random




# Main profile view - shows a user's profile page with their links
async def profile_detail(request, slug):
    try:
        profile, all_links = await get_profile_and_links(slug)
        if not profile or not profile.is_active:
            raise Http404("Profile not found")
        
        # Increment view count 
        await increment_profile_views(slug)
        
        links = [link for link in all_links if link.is_active]
        links.sort(key=lambda x: (x.order, -x.created_at if x.created_at else 0))
        
        context = {
            'profile': profile,
            'links': links,
            'total_clicks': sum(link.click_count for link in links),
        }
        return render(request, 'app/profile_detail.html', context)
    except Exception as e:
        messages.error(request, f"Error loading profile: {str(e)}")
        raise Http404("Profile not found")


async def profile_edit(request, slug):
    profile, all_links = await get_profile_and_links(slug)
    if not profile:
        raise Http404("Profile not found")
    
    links = list(all_links)
    links.sort(key=lambda x: (x.order, -x.created_at if x.created_at else 0))
    
    if request.method == 'POST':
        # Update profile name
        new_name = request.POST.get('profile_name', '').strip()
        if new_name and new_name != profile.full_name:
            await rename_profile(slug, new_name)
            messages.success(request, 'Profile name updated!')
        
        # Update profile bio
        new_bio = request.POST.get('profile_bio', '').strip()
        if new_bio != profile.bio:
            await update_profile_bio(slug, new_bio)
            messages.success(request, 'Profile bio updated!')
    
    context = {
        'profile': profile,
        'links': links,
        'emoji_options': ['🌟', '⚡', '🚀', '💎', '🔥', '🌈', '🎨', '🎭', '🎪', '🎯'],
    }
    return render(request, 'app/profile_edit.html', context)


async def add_link(request, slug):
    if request.method != 'POST':
        raise Http404("Method not allowed")
    
    title = request.POST.get('title', '').strip()
    url = request.POST.get('url', '').strip()
    emoji = request.POST.get('emoji', '🔗').strip()
    link_type = request.POST.get('link_type', 'other')
    description = request.POST.get('description', '').strip()
    
    if title and url and description:
        formatted_url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        await create_link(slug, title, formatted_url, emoji, link_type, description)
        messages.success(request, f'Added link: {emoji} {title}')
    else:
        messages.error(request, 'Title, URL, and description are all required!')
    
    return HttpResponseRedirect(reverse('profile_edit', kwargs={'slug': slug}))


async def delete_link_view(request, slug, link_id):
    if request.method != 'POST':
        raise Http404("Method not allowed")
        
    await delete_link(int(link_id), profile_slug=slug)
    return HttpResponseRedirect(reverse('profile_edit', kwargs={'slug': slug}))


async def update_link_order(request, slug):
    if request.method != 'POST':
        return JsonResponse({'success': False})
        
    from .stately_client import update_link_order
    
    if request.content_type == 'application/json':
        import json
        data = json.loads(request.body)
        link_orders = data.get('orders', [])
        
        for item in link_orders:
            link_id = item.get('id')
            order = item.get('order')
            await update_link_order(int(link_id), order, slug)
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})


async def link_redirect(request, slug, link_id):
    link = await get_link_by_id(int(link_id), slug)
    if not link or not link.is_active:
        raise Http404("Link not found")
    
    # Increment click count (no need to wait for completion)
    await increment_link_clicks(int(link_id), slug)
    
    # Use manual redirect to support mailto: and other protocols
    response = HttpResponse(status=302)
    response['Location'] = link.url
    return response


class HomeView(TemplateView):
    template_name = 'app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_profiles'] = []
        return context


async def create_profile_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            slug = slugify(name)
            profile_image = random.choice(['🌟', '⚡', '🚀', '💎', '🔥', '🌈', '🎨', '🎭'])
            
            profile = await create_profile(name, slug, profile_image)
            
            # Add some sample links
            sample_links = [
                {'title': 'StatelyDB Docs', 'description': 'Learn more about StatelyDB', 'url': 'https://docs.stately.cloud/api/put/', 'emoji': '😎', 'link_type': 'website'},
                {'title': 'Contact Stately', 'description': 'Get in touch with us', 'url': 'mailto:support@stately.cloud', 'emoji': '📧', 'link_type': 'contact'},
            ]
            
            for link_data in sample_links:
                await create_link(
                    slug,
                    link_data['title'],
                    link_data['url'],
                    link_data['emoji'],
                    link_data['link_type'],
                    link_data['description']
                )
            
            messages.success(request, f'Created profile: {name}!')
            return HttpResponseRedirect(reverse('profile_edit', kwargs={'slug': slug}))
    
    return render(request, 'app/create_profile.html')
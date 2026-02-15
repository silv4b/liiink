from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Link, Profile
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "links/home.html")


@login_required
def dashboard(request):
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    links = Link.objects.filter(user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            color = request.POST.get("primary_color")
            if color:
                profile.primary_color = color
                profile.save()
                messages.success(request, "Cor do perfil atualizada!")
                return redirect("dashboard")

        elif action == "add_link":
            if links.count() >= 6:
                messages.error(request, "Você já atingiu o limite de 6 links.")
                return redirect("dashboard")

            title = request.POST.get("title")
            url = request.POST.get("url")
            description = request.POST.get("description", "")
            icon_name = request.POST.get("icon_name", "link")

            if title and url:
                Link.objects.create(
                    user=request.user,
                    title=title,
                    url=url,
                    description=description,
                    icon_name=icon_name,
                )
                messages.success(request, "Link adicionado com sucesso!")
                return redirect("dashboard")

    return render(request, "links/dashboard.html", {"links": links, "profile": profile})


@login_required
def delete_link(request, link_id):
    link = get_object_or_404(Link, id=link_id, user=request.user)
    link.delete()
    messages.success(request, "Link removido.")
    return redirect("dashboard")


@login_required
def edit_link(request, link_id):
    link = get_object_or_404(Link, id=link_id, user=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        url = request.POST.get("url")
        description = request.POST.get("description", "")
        icon_name = request.POST.get("icon_name", "link")

        if title and url:
            link.title = title
            link.url = url
            link.description = description
            link.icon_name = icon_name
            link.save()
            messages.success(request, "Link atualizado com sucesso!")
        else:
            messages.error(request, "Título e URL são obrigatórios.")

    return redirect("dashboard")


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    links = Link.objects.filter(user=user)
    return render(
        request,
        "links/public_profile.html",
        {"profile_user": user, "profile": profile, "links": links},
    )


@login_required
@require_POST
def set_theme_preference(request):
    """Save user's theme preference to the database"""
    import json

    try:
        data = json.loads(request.body)
        theme = data.get("theme")

        if theme not in ["light", "dark", "system"]:
            return JsonResponse(
                {"success": False, "error": "Invalid theme"}, status=400
            )

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.theme_preference = theme
        profile.save()

        return JsonResponse({"success": True, "theme": theme})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

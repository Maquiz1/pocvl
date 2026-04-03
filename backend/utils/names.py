def get_user_display_name(user):
    """
    Returns full name with prefix safely.
    Works even if user has no profile.
    """

    try:
        profile = user.profile
    except user.__class__.profile.RelatedObjectDoesNotExist:
        profile = None

    prefix = ""
    middle = ""

    if profile:
        prefix = profile.prefix.name if profile.prefix else ""
        middle = getattr(profile, "middle_name", "") or ""

    full_name = " ".join(
        part for part in [
            prefix,
            user.first_name,
            middle,
            user.last_name
        ] if part
    ).strip()

    return full_name or user.username
def project_image_upload_path(instance, filename):
    filefolder = 'project-featured-image'
    user = instance.owner.profile.user

    """Add user folder too"""
    return f"{filefolder}/{user}/{instance}/{filename}"

def profile_image_upload_path(instance, filename):
    filefolder = 'user-profile-images'

    """Add user folder too"""
    return f"{filefolder}/{instance}/{filename}"
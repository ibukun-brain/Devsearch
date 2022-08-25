def paginate(page, num_pages):
    custom_range = None
    leftIndex = (int(page) - 4)
    rightIndex = (int(page) + 5)
    if page is None:
        page = page
        if leftIndex < 1:
            leftIndex = 1

        if rightIndex > num_pages:
            rightIndex = num_pages + 1
    else:
        page = page

        if leftIndex < 1:
            leftIndex = 1

        if rightIndex > num_pages:
            rightIndex = num_pages + 1

        
        custom_range = range(leftIndex, rightIndex)
    # custom_range
    return custom_range
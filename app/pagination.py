def paginate_query(query, page, limit):
    page = int(page)
    limit = int(limit)

    total_items = query.count()
    total_pages = (total_items + limit - 1) // limit

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
        "data": items
    }


def paginate_list(data, page, limit):
    page = int(page)
    limit = int(limit)

    total_items = len(data)
    total_pages = (total_items + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    items = data[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
        "data": items
    }

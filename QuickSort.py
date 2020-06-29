def quick_sort(array, left, right):
    if left >= right:
        return
    l, r = left, right
    pivot = array[l]
    while l < r:
        while l < r and array[r] >= pivot:
            r = r - 1
        if l < r:
            array[l] = array[r]
        while l < r and array[l] <= pivot:
            l = l + 1
        if l < r:
            array[r] = array[l]
        if l >= r:
            array[l] = pivot
    quick_sort(array, left, r - 1)
    quick_sort(array, r + 1, right)


Array = [19, 97, 9, 17, 1, 8, 103, 34]
quick_sort(Array, 0, 7)
print(Array)

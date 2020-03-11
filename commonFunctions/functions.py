def fixString(string):
    stringArr = [i for i in string]
    badIndexes = [i for i in range(
        len(stringArr)) if stringArr[i] == '\'']
    for i in range(len(badIndexes)-1, -1, -1):
        stringArr.insert(badIndexes[i], "\\")
    return ''.join(stringArr)


def searchIndex(arr, val, key):
    l = 0
    r = len(arr)-1
    while r-l > 1:
        m = (r+l)//2
        if arr[m][key] < val:
            l = m
        else:
            r = m
    if arr[r][key] > val:
        return r-1
    return r

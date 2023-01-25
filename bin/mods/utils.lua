function string.startsWith(str, prefix)
    return string.find(str, prefix, string.len(prefix), true) ~= nil
end

function string.endsWith(str, suffix)
    return string.find(str, suffix, -string.len(suffix), true) ~= nil
end

function string.split(str, sep, maxsplit)
    local str = tostring(str)
    local sep = tostring(sep)
    local maxsplit = tonumber(maxsplit) or -1
    local p = 1
    local targetArray = {}
    if (sep == nil) then
        return false
    end
    while (true) do
        si, sd = string.find(str, sep, p, true) -- plain find
        if (si) then
            table.insert(targetArray, string.sub(str, p, si - 1))
            p = sd + 1
        else
            table.insert(targetArray, string.sub(str, p, string.len(str)))
            break
        end
        maxsplit = maxsplit - 1
        if (maxsplit == 0) then
            table.insert(targetArray, string.sub(str, p, string.len(str)))
            break
        end
    end
    return targetArray
end
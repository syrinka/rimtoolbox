local p = {}

local function html()
    return mw.html.create()
end

local function header(label, className)
    if (not className) then
        className = 'infobox-header'
    end

    return html()
    :tag('tr')
        :addClass(className)
        :tag('th')
            :css('padding', '8px')
            :attr('colspan', 2)
            :wikitext(label)
        :done()
    :done()
end

local function line(label, value)
    return html()
    :tag('tr')
        :tag('th')
            :addClass('infobox-label')
            :cssText('font-size:12px;padding:4px;text-align:right;width:110px;')
            :tag('span')
                :addClass('bg-primary')
                :cssText('margin-left:4px;padding:2px;color:#000;')
                :wikitext(label)
            :done()
        :done()
        :tag('td')
            :addClass('infobox-data')
            :cssText('font-size:12px;padding:4px')
            :wikitext(value)
        :done()
    :done()
end

function a(href, label)
    -- mw.html.wikitext does not originally support redirect syntax `[[]]`
    -- this function replenish it
    -- @TODO
end

function p.render(defName)
    local data = mw.huiji.db.findOne({
        ['_id'] = 'Data:ThingDef/'..defName..'.json',
    })
    local order = mw.huiji.db.findOne({
        ['_id'] = 'Data:StatOrder.json'
    }).order

    local box = html():tag('table')
        :addClass('infobox')
    	:css('width', '350px')
        :css('font-size', '14px')

    local tab = html()
    -- title
    :node(header(data['label-zh'], 'infobox-title'))
    -- graphic
    :tag('tr'):tag('td')
        :attr('colspan', 2)
        :css('text-align', 'center')
        :tag('small')
            :css('text-align', 'center')
            -- :wikitext(data['description-zh'])
        :done()
    :done():done()
    -- description
    :tag('tr'):tag('td')
        :attr('colspan', 2)
        :css('text-align', 'center')
        :tag('small')
            :wikitext(data['description-zh'])
        :done()
    :done():done()
    -- infos
    tab:node(header('基本信息'))
        -- seems like there's only one item in `thingCategories`
        :node(line('类型', '[['..data.category..']] - [['..data.thingCategories[1]..']]'))

    local stats = data.statBases
    for _, section in pairs(order) do
        if (section.children) then
            local collect = {} -- list
            for _, child in pairs(section.children) do
                if (stats[child.defName]) then
                    table.insert(collect, {
                        ['label'] = child.label,
                        ['value'] = stats[child.defName]
                    })
                end
            end
            if (#collect ~= 0) then
                mw.log(section.label)
                mw.logObject(collect)
                tab:node(header(section.label))
                for _, dat in pairs(collect) do
                    tab:node(line(dat['label'], dat['value']))
                end
            end
        end
    end

    return tostring(box:node(tab))
end

function p.box(frame)
    local defName = frame.args[1]
    return p.render(defName)
end

return p
-- trie.lua
local TrieNode = {}
TrieNode.__index = TrieNode

function TrieNode.new()
    return setmetatable({children = {}, isEndOfWord = false}, TrieNode)
end

local Trie = {}
Trie.__index = Trie

function Trie.new()
    return setmetatable({root = TrieNode.new()}, Trie)
end

function Trie:insert(word)
    local node = self.root
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then
            node.children[char] = TrieNode.new()
        end
        node = node.children[char]
    end
    node.isEndOfWord = true
end

function Trie:search(word)
    local node = self.root
    for i = 1, #word do
        local char = word:sub(i, i)
        if not node.children[char] then
            return false
        end
        node = node.children[char]
    end
    return node.isEndOfWord
end

function Trie:startsWith(prefix)
    local node = self.root
    for i = 1, #prefix do
        local char = prefix:sub(i, i)
        if not node.children[char] then
            return false
        end
        node = node.children[char]
    end
    return true
end

local function collectWords(node, prefix)
    local words = {}
    if node.isEndOfWord then
        table.insert(words, prefix)
    end
    for char, child in pairs(node.children) do
        local childWords = collectWords(child, prefix .. char)
        for _, word in ipairs(childWords) do
            table.insert(words, word)
        end
    end
    return words
end

function Trie:groupByCommonPrefix()
    local groups = {}

    local function group(node, prefix)
        if next(node.children) and next(node.children, next(node.children)) then
            local words = collectWords(node, prefix)
            groups[prefix] = words
        end
        for char, child in pairs(node.children) do
            group(child, prefix .. char)
        end
    end

    group(self.root, "")
    return groups
end

return Trie

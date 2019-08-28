//
// Hobo File System
//
// (C) Copyright 2019 Tony Mason
//
// Licensed under the Aranae project license
// https://github.com/fsgeek/Araneae/blob/master/LICENSE
//
#pragma once

#if !defined(__HOBO_LIST_H__)
#define __HOBO_LIST_H__ (1)

#include <assert.h>

#if !defined(FORCEDINLINE)
#define FORCEDINLINE __attribute__((always_inline)) inline
#endif // FORCEDINLINE

typedef struct _list_entry_t list_entry_t;

struct _list_entry_t {
    list_entry_t *next;
    list_entry_t *prev;
};


FORCEDINLINE int empty_list(list_entry_t *entry)
{
    return entry->next == entry;
}

FORCEDINLINE list_entry_t *list_head(list_entry_t *list)
{
    return list->next;
}

#define list_for_each(_list, _itr)                                      \
    for ((_itr) = list_head((_list));                                   \
         (_itr) != (_list);                                             \
         (_itr) = (_itr)->next)



FORCEDINLINE void initialize_list_entry(list_entry_t *entry)
{
    entry->next = entry->prev = entry;
}

#define initialize_list(l) initialize_list_entry(l)

FORCEDINLINE void verify_list_entry(list_entry_t *entry)
{
    assert(entry->next->prev == entry);
    assert(entry->prev->next == entry);
}

FORCEDINLINE int remove_list_entry(list_entry_t *entry)
{
    list_entry_t *prev, *next;

    verify_list_entry(entry);

    next = entry->next;
    prev = entry->prev;

    next->prev = prev;
    prev->next = next;

    entry->next = entry->prev = entry;

    if (next == prev) {
        return 1;
    }
    return 0;
}

FORCEDINLINE list_entry_t *remove_list_head(list_entry_t *list)
{
    list_entry_t *entry = list->next;
    remove_list_entry(entry);
    return entry;
}

FORCEDINLINE list_entry_t *remove_tail_list(list_entry_t *list)
{
    list_entry_t *entry = list->prev;
    remove_list_entry(entry);
    return entry;
}

FORCEDINLINE void insert_list_tail(list_entry_t *list, list_entry_t *entry)
{
    verify_list_entry(list);
    verify_list_entry(list->next);
    verify_list_entry(list->prev);
    entry->next = list;
    entry->prev = list->prev;
    entry->prev->next = entry;
    list->prev = entry;
    verify_list_entry(list);
    verify_list_entry(entry);
}

FORCEDINLINE void insert_list_head(list_entry_t *list, list_entry_t *entry)
{
    verify_list_entry(list);
    verify_list_entry(list->next);
    verify_list_entry(list->prev);
    entry->prev = list;
    entry->next = list->next;
    entry->next->prev = entry;
    list->next = entry;
    verify_list_entry(list);
    verify_list_entry(entry);

}

#endif // __HOBO_LIST_H__

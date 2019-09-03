//
// Hobo File System
//
// (C) Copyright 2019 Tony Mason
//
// Licensed under the Aranae project license
// https://github.com/fsgeek/Araneae/blob/master/LICENSE
//

#include "hobo.h"
#include <whitedb/dbapi.h>
#include <uuid/uuid.h>

hobo_object_t *root_hob = NULL;

static const char *hobo_root_uuid_str = "719d92f9-1964-49db-981d-b4bd7744951b";

// #define UUID_DEFINE(name,u0,u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12,u13,u14,u15)
//        static const uuid_t name __attribute__ ((unused)) = {u0,u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12,u13,u14,u15}

uuid_t hobo_root_uuid = {0x71, 0x9d, 0x92, 0xf9, 0x19, 0x64, 0x49, 0xdb, 0x98, 0x1d, 0xb4, 0xbd, 0x77, 0x44, 0x95, 0x1b};

static struct stat root_statbuf;
void *hobo_db;
static const char *hobo_db_name = "hobo";

static void init(void *userdata, struct fuse_conn_info *conn)
{
    static int initialized = 0;
    char dbname[16];
    uuid_t test_uuid;

    fprintf(stderr, "HoboFS: called %s, userdata = 0x%p, conn = 0x%p\n",__PRETTY_FUNCTION__, userdata, conn);

    // TODO: initialization

    while (!initialized) {
        // initialization logic goes here
        uuid_parse(hobo_root_uuid_str, test_uuid);
        assert(0 == uuid_compare(test_uuid, hobo_root_uuid));

        root_statbuf.st_ino = FUSE_ROOT_ID;
        root_statbuf.st_mode = S_IFDIR | 0755;
        root_statbuf.st_nlink = 1;
        root_statbuf.st_uid = getuid();
        root_statbuf.st_gid = getgid();
        root_statbuf.st_size = 0x1000;
        root_statbuf.st_blocks = 1;
        root_statbuf.st_atime = time(NULL);
        root_statbuf.st_mtime = root_statbuf.st_atime;
        root_statbuf.st_ctime = root_statbuf.st_ctime;

        root_hob = hobo_object_create(FUSE_ROOT_ID, NULL, &root_statbuf);
        assert(NULL != root_hob);

        // TODO: this is where I'd want to load in any initial state from the persistent store
        memset(dbname, 0, sizeof(dbname));
        strncpy(dbname, hobo_db_name, sizeof(dbname) - sizeof(char)); // the annoyance of APIs that take non-const strings - can't pass it directly w/o a compiler warning.
        wg_delete_database(dbname); // always start with a clean database
        hobo_db = wg_attach_database(dbname, 200 * 1024 * 1024); // 200MB for now, not sure about the name
        assert(NULL != hobo_db);

        //
        // Done
        //
        initialized = 1;
    }
}

hobo_init_t hobo_init = init;

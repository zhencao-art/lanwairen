#ifndef __PROTO_H__
#define __PROTO_H__

#include <stdint.h>

#ifndef MAX_DISKID
#define MAX_DISKID 128
#endif

#ifndef MAX_IP
#define MAX_IP 32
#endif

struct protohead {
    uint32_t size;
    uint32_t cmd;
    uint64_t sector;
    uint64_t secnum;
    uint64_t flowno;
    uint32_t magic;
    int retcode;
    char data[0];
}  __attribute__ ((packed));

struct proto_stat {
    char udisk_id[MAX_DISKID];
    char udisk_ip[MAX_IP];
    unsigned short udisk_port;
} __attribute__ ((packed));

enum MIGRATE_UBS_ACTION {       // must be sync'ed with message definition!!!!!
    MIGRATE_UBS_NULL = 10,
    MIGRATE_UBS_START = 20,
    MIGRATE_UBS_TERM = 30,
    MIGRATE_UBS_DONE = 40,       // proxy response back to master that it is done.
};

enum {
    PIGGY_MIGRATE_UBS = 1,      // same with proxy definition
};

struct udisk_gate_piggy_migrate_ubs {
    uint32_t piggy;                     // all piggy should start with this flag
    char ip[MAX_IP];
    unsigned short port;
    unsigned short action;
}  __attribute__ ((packed));

enum {
    CMD_READ = 0,
    CMD_WRITE = 1,
    CMD_STAT = 2,
    CMD_NOP = 3,
    CMD_FLUSH = 4,
    CMD_GET_IP = 10,
};



enum {
    MAGIC_NUMBER = 0xf123987a,
};

#ifdef __cplusplus
extern "C" {
#endif

struct protohead *make_read_request(uint64_t sector, uint64_t secnum, uint64_t *flowno);
struct protohead *make_read_response(uint64_t sector, uint64_t secnum, const char* data, uint64_t flowno, int retcode);
struct protohead *make_write_request(uint64_t sector, uint64_t secnum, const char *data, uint64_t *flowno);
struct protohead *make_write_response(uint64_t sector, uint64_t secnum, uint64_t flowno, int retcode);
struct protohead *make_stat_request(uint64_t *flowno);
struct protohead *make_stat_response(uint64_t flowno, int retcode);
struct protohead *make_flush_response(uint64_t flowno, int retcode);
void dump_head(struct protohead *head);
void dump_data(struct protohead *head);
uint64_t gen_flowno();
#ifdef __cplusplus
}
#endif

#ifndef SECTOR_SIZE
#define SECTOR_SIZE 512ull
#endif

#endif


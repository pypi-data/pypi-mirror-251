#ifndef DASH_H
#define DASH_H

#define PY_SSIZE_T_CLEAN

#ifdef __cplusplus
extern "C" {
#endif

void dash_hash(const char* input, int len, char* output);

#ifdef __cplusplus
}
#endif

#endif

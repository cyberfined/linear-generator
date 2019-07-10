# linear-generator
python script for generate c matrix library

# Usage
To generate library call genLinearLib in main.py.

```
genLinearLib(name, vecs)
```

first argument is a name of .h and .c files, second is a list of essences, which will be generated.

## Essences
There are two essences, the first one is vector in vector.py, the second one is matrix in matrix.py.

```
Vector(size, scalar, funcs)
Matrix(rows, cols, scalar, funcs)
```

To create an essence you must specify size, type(int,float,double) and functions, which iterate over essence. All functions are located in funcType.py.

## Functions

Name | c prototype | description
--- | --- | ---
zero | vec zero() | create vector or matrix with all zero components
identity | mat identity() | create identity matrix
transpose | mat transpose(mat m) | transpose given matrix
mmult | vec mmult(mat m, vec v) | multiply vector by matrix or matrix by matrix
translate | mat translate(vec v) |  create translation matrix
mat44rotate | mat44 mat44_rotate(vec axis, float a) | create 4x4 rotation matrix
mat44perspective | mat44 mat44_perspective(scalar a, scalar ratio, scalar n, scalar f) | create 4x4 perspective projection matrix
lcons | vec lcons(vec v, scalar s) | create vector from one less dimension vector and scalar
add | vec add(vec a, vec b) | return sum of two vectors or matrices
sub | vec sub(vec a, vec b) | return difference between two vectors or matrices
smult | vec smult(vec v, scalar s) | return vector or matrix multiplied by scalar
interpolate | vec interpolate(vec a, vec b, scalar t) | return vector or matrix calculated by a + (b-a)*t
dot | scalar dot(vec a, vec b) | return dot product
vec3cross | vec3 vec3_cross(vec3 a, vec3 b) | return cross product of a and b
sqlength | scalar sqlength(vec v) | return squared vector's length
length | scalar length(vec v) | return vector's length
normalize | vec normalize(vec v) | return normalized vector
proj | vec proj(vec v) | return one less dimension vector by dropping last component
hom | vec hom(vec v) | return one less dimension vector by dividing all components by the last one and then dropping it

where:
* vec is either vector or matrix
* mat is a matrix
* scalar is int, float or double

## Example
Let's generate 3d vector, 4d vector with constructor from 3d vector, add, sub and smult functions and 4x4 matrix with zero, identity, mmult and perspective functions.

```python
if __name__ == "__main__":
    v3f = vector.vec3f()
    v4f = vector.vec4f(funcType.funcList("lcons", "add", "sub", "smult"))
    mat44f = matrix.mat44f(funcType.funcList(
        "zero",
        "identity",
        ["mmult", "mat44f_mult", "mat44f", 4, 4],
        ["mmult", "mat44fv4_mult", "vec4f", 4, 1],
        "mat44perspective"
    ))
    genLinearLib("linear", [v3f, v4f, mat44f])
```

Consider in more details mmult. If you give list instead of string, first value of it must be the name of function, another values are parameters for generator. In our case second value is a name of generated function, third value is a return type, fourth and fifth values are rows and columns of resulted essence. In result next files will be generated:

### linear.h file
```c
#pragma once

typedef struct { float x,y,z; } vec3f;
typedef struct { float x,y,z,w; } vec4f;
typedef struct { vec4f X,Y,Z,W; } mat44f;

vec3f Vec3f(float x, float y, float z);

vec4f Vec4f(float x, float y, float z, float w);
vec4f Vec4f3(vec3f v, float s);
vec4f vec4f_add(vec4f a, vec4f b);
vec4f vec4f_sub(vec4f a, vec4f b);
vec4f vec4f_smult(vec4f v, float k);

mat44f Mat44f(vec4f X, vec4f Y, vec4f Z, vec4f W);
mat44f mat44f_zero();
mat44f mat44f_identity();
mat44f mat44f_mult(mat44f m, mat44f a);
vec4f mat44fv4_mult(mat44f m, vec4f a);
mat44f mat44f_perspective(float angle, float aratio, float near, float far);
```

### linear.c file
```c
#include "linear.h"
#include <stddef.h>
#include <math.h>

static void generic_float_add(float *a, float *b, float *out, size_t n) {
    for(size_t i = 0; i < n; i++) out[i] = a[i] + b[i];
}

static void generic_float_sub(float *a, float *b, float *out, size_t n) {
    for(size_t i = 0; i < n; i++) out[i] = a[i] - b[i];
}

static void generic_float_smult(float *v, float k, float *out, size_t n) {
    for(size_t i = 0; i < n; i++) out[i] = v[i] * k;
}

static void generic_float_zero(float *out, size_t n) {
    for(size_t i = 0; i < n; i++) out[i] = 0;
}

static void generic_float_identity(float *out, size_t n) {
    generic_float_zero(out, n*n);
    for(size_t i = 0; i < n; i++) out[i*n + i] = 1;
}

static void generic_float_mmult(float *a, float *b, float *out, size_t r1, size_t c1, size_t r2, size_t c2) {
    for(size_t i = 0; i < r1; i++)
        for(size_t j = 0; j < c2; j++)
            for(size_t k = 0; k < c1; k++)
                out[i*c2 + j] += a[i*c1 + k] * b[k*c2 + j];
}

vec3f Vec3f(float x, float y, float z) { return (vec3f) { x, y, z }; }

vec4f Vec4f(float x, float y, float z, float w) { return (vec4f) { x, y, z, w }; }

vec4f Vec4f3(vec3f v, float s) { return (vec4f){ v.x, v.y, v.z, s }; }

vec4f vec4f_add(vec4f a, vec4f b) {
    vec4f out;
    generic_float_add((float*)&a, (float*)&b, (float*)&out, 4);
    return out;
}

vec4f vec4f_sub(vec4f a, vec4f b) {
    vec4f out;
    generic_float_sub((float*)&a, (float*)&b, (float*)&out, 4);
    return out;
}

vec4f vec4f_smult(vec4f v, float k) {
    vec4f out;
    generic_float_smult((float*)&v, k, (float*)&out, 4);
    return out;
}

mat44f Mat44f(vec4f X, vec4f Y, vec4f Z, vec4f W) { return (mat44f) { X, Y, Z, W }; }

mat44f mat44f_zero() {
    mat44f out;
    generic_float_zero((float*)&out, 16);
    return out;
}

mat44f mat44f_identity() {
    mat44f out;
    generic_float_identity((float*)&out, 4);
    return out;
}

mat44f mat44f_mult(mat44f m, mat44f a) {
    mat44f out;
    generic_float_mmult((float*)&m, (float*)&a, (float*)&out, 4, 4, 4, 4);
    return out;
}

vec4f mat44fv4_mult(mat44f m, vec4f a) {
    vec4f out;
    generic_float_mmult((float*)&m, (float*)&a, (float*)&out, 4, 4, 4, 1);
    return out;
}

mat44f mat44f_perspective(float angle, float aratio, float near, float far) {
    float f = 1.0/tan(angle/2.0);
    return (mat44f) {
        {f/aratio, 0, 0, 0},
        {0, f, 0, 0},
        {0, 0, (far+near)/(near-far), -1},
        {0, 0, 2*far*near/(near-far), 0}
    };
}
```
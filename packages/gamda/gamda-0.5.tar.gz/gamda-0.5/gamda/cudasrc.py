"""
    The source of the cuda code for including
"""

INCLUDE = r"""#define INT_NAN -999999
__device__ int isnan(int a)
{
    return a == INT_NAN;

}
__device__ float get_distance(const float* local_position, int a, int b)
{
    float dx = local_position[a * 3] - local_position[b * 3];
    float dy = local_position[a * 3 + 1] - local_position[b * 3 + 1];
    float dz = local_position[a * 3 + 2] - local_position[b * 3 + 2];
    return norm3df(dx, dy, dz);
}

__device__ float get_distance(const float* local_position, int a, int b, const float* dimension)
{
    float dx = local_position[a * 3] - local_position[b * 3];
    float dy = local_position[a * 3 + 1] - local_position[b * 3 + 1];
    float dz = local_position[a * 3 + 2] - local_position[b * 3 + 2];
    dx -= floorf(dx / dimension[0] + 0.5) * dimension[0];
    dy -= floorf(dy / dimension[1] + 0.5) * dimension[1];
    dz -= floorf(dz / dimension[2] + 0.5) * dimension[2];
    return norm3df(dx, dy, dz);
}

#ifdef GOOD_N_FRAME
__device__ float FramewiseAtomicAdd(float* ptr, float v)
{
    for (int mask = GOOD_N_FRAME / 2; mask > 0; mask /= 2)
        v += __shfl_down_sync(0xFFFFFFFF, v, mask);
    if (threadIdx.y == 0)
    {
        atomicAdd(ptr, v);
    }
}
#else
#define FramewiseAtomicAdd atomicAdd
#endif
"""
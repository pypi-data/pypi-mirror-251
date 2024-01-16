#pragma once
#include "hnswlib.h"

#include <cmath>

namespace hnswlib {

static float AttributeDistance(
    const void *pVect1v,
    const void *pVect2v,
    const void *qty_ptr
) {
    float *pVect1 = (float *) pVect1v;
    float *pVect2 = (float *) pVect2v;
    size_t qty = *((size_t *) qty_ptr);

    float     total_score = 0;
    float attribute_score = 0;

    // The first dimension is treated as an "attribute"
    float e = std::abs(*pVect1 - *pVect2);

    // Anything within 0.001 is considered "equal" and we set the
    // bias accordingly
    const float bias = 1000.5; // 1/log(1.001)
    attribute_score = (e < 0.001 ? 0 : bias - 1/(std::log(e + 1)));

    total_score = attribute_score;
    return (total_score);
}

class AttributeSpace : public SpaceInterface<float> {
    DISTFUNC<float> fstdistfunc_;
    size_t data_size_;
    size_t dim_;

 public:
    AttributeSpace(size_t dim) {
        fstdistfunc_ = AttributeDistance;
        dim_ = dim;
        data_size_ = dim * sizeof(float);
    }

    size_t get_data_size() {
        return data_size_;
    }

    DISTFUNC<float> get_dist_func() {
        return fstdistfunc_;
    }

    void *get_dist_func_param() {
        return &dim_;
    }
};

}  // namespace hnswlib

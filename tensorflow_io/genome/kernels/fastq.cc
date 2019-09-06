#include <vector>
#include <string>

#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include "tensorflow/core/framework/op_kernel.h"
#include "nucleus/io/fastq_reader.h"
#include "nucleus/platform/types.h"
#include "nucleus/protos/fastq.pb.h"
#include "nucleus/util/utils.h"
#include <utility> 

namespace tensorflow {

using nucleus::FastqReader;
using nucleus::genomics::v1::FastqRecord;

class FastqOp : public OpKernel {
  public:
    explicit FastqOp(OpKernelConstruction* context) : OpKernel(context) {}
    ~FastqOp() {}

    void Compute(OpKernelContext* context) override {

      const Tensor& filename_tensor = context->input(0);
      const std::string& filename = filename_tensor.scalar<string>()();

      std::unique_ptr<FastqReader> reader = std::move(
        FastqReader::FromFile(filename,
                              nucleus::genomics::v1::FastqReaderOptions())
            .ValueOrDie());

      std::vector<std::string> sequences;
      std::vector<std::string> quality;

      std::shared_ptr<nucleus::FastqIterable> iterable = reader->Iterate().ValueOrDie();
      for (const nucleus::StatusOr<FastqRecord*> maybe_sequence : iterable) {
        OP_REQUIRES(context, maybe_sequence.ok(), errors::Internal("internal error: ", maybe_sequence.error_message()));
        sequences.push_back(maybe_sequence.ValueOrDie()->sequence());
        quality.push_back(maybe_sequence.ValueOrDie()->quality());
      }

      TensorShape output_shape({static_cast<int64>(sequences.size())});
      Tensor* output_tensor;
      Tensor* quality_tensor;
      OP_REQUIRES_OK(context, context->allocate_output(0, output_shape, &output_tensor));
      OP_REQUIRES_OK(context, context->allocate_output(1, output_shape, &quality_tensor));

      for (size_t i = 0; i < sequences.size(); i++) {
        output_tensor->flat<string>()(i) = std::move(sequences[i]);
        quality_tensor->flat<string>()(i) = std::move(quality[i]);
      }
    }
};

REGISTER_OP("FastqOp")
    .Input("filename: string")
    .Output("sequences: string")
    .Output("raw_quality: string")
    .SetShapeFn([](::tensorflow::shape_inference::InferenceContext* c) {
      c->set_output(0, c->MakeShape({c->UnknownDim()}));
      return Status::OK();
    });
REGISTER_KERNEL_BUILDER(Name("FastqOp").Device(DEVICE_CPU), FastqOp);

} // tensorflow

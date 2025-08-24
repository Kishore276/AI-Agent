#!/usr/bin/env python3
"""
Verify CUDA installation and RTX 2050 GPU availability
"""

import sys

def verify_cuda():
    """Verify CUDA installation and GPU availability"""
    print("🔍 Verifying CUDA Installation...")
    print("=" * 50)
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        print(f"🚀 CUDA available: {cuda_available}")
        
        if cuda_available:
            # Get GPU information
            gpu_count = torch.cuda.device_count()
            print(f"📊 GPU count: {gpu_count}")
            
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
                print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
            # Check if RTX 2050 is detected
            current_gpu = torch.cuda.get_device_name(0)
            if 'RTX 2050' in current_gpu:
                print("✅ RTX 2050 detected and ready for training!")
                
                # Test GPU functionality
                print("\n🧪 Testing GPU functionality...")
                try:
                    # Create a test tensor on GPU
                    test_tensor = torch.randn(1000, 1000).cuda()
                    result = torch.matmul(test_tensor, test_tensor.T)
                    print("✅ GPU computation test passed")
                    
                    # Check memory
                    memory_allocated = torch.cuda.memory_allocated() / 1024**2
                    memory_reserved = torch.cuda.memory_reserved() / 1024**2
                    print(f"💾 GPU Memory - Allocated: {memory_allocated:.1f}MB, Reserved: {memory_reserved:.1f}MB")
                    
                    # Clear memory
                    del test_tensor, result
                    torch.cuda.empty_cache()
                    print("🧹 GPU memory cleared")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ GPU computation test failed: {e}")
                    return False
            else:
                print(f"⚠️  Expected RTX 2050, found: {current_gpu}")
                return False
        else:
            print("❌ CUDA not available - GPU training not possible")
            return False
            
    except ImportError as e:
        print(f"❌ PyTorch not installed or import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main verification function"""
    success = verify_cuda()
    
    if success:
        print("\n🎉 CUDA verification successful!")
        print("🚀 Ready to run RTX 2050 GPU training:")
        print("   python train_rtx2050_gpu.py")
    else:
        print("\n❌ CUDA verification failed")
        print("🛑 GPU training not possible")
        sys.exit(1)

if __name__ == "__main__":
    main()

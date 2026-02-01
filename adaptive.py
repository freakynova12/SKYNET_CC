
class AdaptivePolicy:
    def __init__(self):
        self.success_threshold=0.8

    def update(self,metrics):
        sr=metrics.get("success_rate",0)
        if sr<0.7: self.success_threshold*=0.95
        elif sr>0.9: self.success_threshold*=1.05
        return self.success_threshold

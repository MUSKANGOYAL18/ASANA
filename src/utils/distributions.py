"""Statistical distribution utilities."""
import numpy as np
from typing import Tuple

class DistributionGenerator:
    """Generate values from various statistical distributions."""
    
    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)
        
    def log_normal(self, median: float, percentile_90: float) -> float:
        """
        Generate value from log-normal distribution.
        
        Args:
            median: Median value
            percentile_90: 90th percentile value
            
        Returns:
            Generated value
        """
        # Calculate mu and sigma from median and 90th percentile
        mu = np.log(median)
        # P(X <= p90) = 0.9, so p90 = exp(mu + 1.28*sigma)
        sigma = (np.log(percentile_90) - mu) / 1.28
        
        return self.rng.lognormal(mu, sigma)
        
    def power_law(self, alpha: float, x_min: float, x_max: float) -> float:
        """
        Generate value from power law distribution.
        
        Args:
            alpha: Power law exponent
            x_min: Minimum value
            x_max: Maximum value
            
        Returns:
            Generated value
        """
        u = self.rng.uniform(0, 1)
        
        if alpha == 1:
            return x_min * np.exp(u * np.log(x_max / x_min))
        else:
            return (x_min**(1-alpha) + u * (x_max**(1-alpha) - x_min**(1-alpha)))**(1/(1-alpha))
            
    def pareto(self, alpha: float, scale: float) -> float:
        """
        Generate value from Pareto distribution.
        
        Args:
            alpha: Shape parameter
            scale: Scale parameter
            
        Returns:
            Generated value
        """
        return self.rng.pareto(alpha) * scale + scale
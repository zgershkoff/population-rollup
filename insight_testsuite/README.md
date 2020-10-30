# Test cases

1. Provided to begin with.
2. A data sheet with no data (except for the header) will generate an empty report.
3. When lines don't have a CBSA, they are not included in the report.
4. Testing how a larger example is handled.
5. What a tract has no recorded population in 2000 or 2010, it's still counted but the percentage change is treated as 0.
6. This tests that rounding is done correctly on the decimal percentage change.
7. This tests that the sorting is done correctly when the tracts are not presented in order.

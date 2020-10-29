from population import calculate_moving_average as cma
from population import _parse_data as pd
import unittest

class TestMovingAverage(unittest.TestCase):

    def test_0_avg(self):
        self.assertEqual(cma(-5, 2, 10), 0)

    def test_unchanged(self):
        val = 100
        self.assertEqual(cma(val, 200, val), val)

    def test_small_change(self):
        self.assertGreater(cma(10**9, 10**6, 10**9+1), 10**9)

    def test_iterations(self):
        val = num = 1
        avg = 1.5
        for i in range(2, 5):
            self.assertEqual(cma(val, num, i), avg)
            val = avg
            num += 1
            avg += 0.5

class TestParseData(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestParseData, self).__init__(*args, **kwargs)
        self.header = ['GEOID', 'ST10', 'COU10', 'TRACT10', 'AREAL10', 'AREAW10', 'CSA09', 'CBSA09', 'CBSA_T', 'MDIV09', 'CSI', 'COFLG', 'POP00', 'HU00', 'POP10', 'HU10', 'NPCHG', 'PPCHG', 'NHCHG', 'PHCHG']
        self.input = [
        ['02130000100', '02', '130', '000100', '4835.518216', '1793.906364', '', '28540', 'Ketchikan, AK', '', '2', 'C', '3801', '1736', '3484', '1694', '-317', '-8.34', '-42', '-2.42'],
        ['02130000200', '02', '130', '000200', '5.204047664', '0.4525275793', '', '28540', 'Ketchikan, AK', '', '2', 'C', '4909', '2156', '4884', '2179', '-25', '-0.51', '23', '1.07'],
        ['02130000300', '02', '130', '000300', '2.771683112', '0.4653222332', '', '28540', 'Ketchikan, AK', '', '2', 'C', '3054', '1493', '2841', '1394', '-213', '-6.97', '-99', '-6.63'],
        ['02130000400', '02', '130', '000400', '14.91968071', '0.3246679135', '', '28540', 'Ketchikan, AK', '', '2', 'C', '2310', '891', '2268', '899', '-42', '-1.82', '8', '0.90'],
        ['48487950300', '48', '487', '950300', '933.9565129', '6.998080686', '', '46900', 'Vernon, TX', '', '2', 'C', '2304', '916', '1849', '892', '-455', '-19.75', '-24', '-2.62'],
        ['48487950500', '48', '487', '950500', '13.21399173', '0.01418539391', '', '46900', 'Vernon, TX', '', '2', 'C', '3172', '1338', '2955', '1388', '-217', '-6.84', '50', '3.74'],
        ['48487950600', '48', '487', '950600', '10.65575478', '0', '', '46900', 'Vernon, TX', '', '2', 'C', '6022', '2715', '5994', '2781', '-28', '-0.46', '66', '2.43'],
        ['48487950700', '48', '487', '950700', '13.01780124', '0.0371546123', '', '46900', 'Vernon, TX', '', '2', 'C', '3181', '1409', '2737', '1257', '-444', '-13.96', '-152', '-10.79']]


    def test_given_example(self):
        input_data = self.input
        CBSAs, data = pd(input_data)
        self.assertEqual(CBSAs, [28540, 46900])
        self.assertEqual(data[CBSAs[1]]["name"], "Vernon, TX")
        self.assertEqual(data[CBSAs[0]]["pop10"], 13477)

    def test_missing_CBSA(self):
        epsilon = 0.00000001
        input_data = self.input
        input_data[0][7] = '' # careful, this isn't a deep copy
        CBSAs, data = pd(input_data)
        self.assertEqual(data[CBSAs[0]]["pop00"], 10273)
        self.assertTrue(data[CBSAs[0]]["change"] <= -3.1 + epsilon)
        self.assertTrue(data[CBSAs[0]]["change"] >= -3.1 - epsilon)
        input_data[0][7] = '28540' # in case future tests want this

    def test_empty_report(self):
        input_data = [self.input[0]]
        input_data[0][7] = ''
        CBSAs, data = pd(input_data)
        self.assertEqual(CBSAs, [])
        self.assertEqual(data, {})


if __name__ == '__main__':
    unittest.main()

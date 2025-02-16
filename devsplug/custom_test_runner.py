from django.test.runner import DiscoverRunner

class CustomTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, **kwargs):
        result = super().run_tests(test_labels, **kwargs)
        if result:
            print("\n========================================")
            print("TESTS FAILED: {} failure(s) detected.".format(result))
            print("Please review the above errors and tracebacks.")
            print("========================================\n")
        else:
            print("\n========================================")
            print("ALL TESTS PASSED SUCCESSFULLY!")
            print("========================================\n")
        return result 
from django.test.runner import DiscoverRunner
from django.utils.termcolors import colorize
import time
from unittest.runner import TextTestResult
import inspect

class CustomTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, **kwargs):
        print("\n" + "="*80)
        print(colorize("🚀 Starting Test Session", fg="cyan", opts=("bold",)))
        print("="*80)
        
        self.start_time = time.time()
        self.test_results = []
        
        result = super().run_tests(test_labels, **kwargs)
        
        self._generate_report()
        return result

    def _generate_report(self):
        print("\n" + "="*80)
        print(colorize("📊 Test Execution Report", fg="magenta", opts=("bold",)))
        print("="*80 + "\n")
        
        # Group tests by module
        modules = {}
        for test in self.test_results:
            module = test['module']
            if module not in modules:
                modules[module] = []
            modules[module].append(test)
        
        # Print results by module
        for module, tests in modules.items():
            print(colorize(f"📁 {module}", fg="yellow", opts=("bold",)))
            print("-" * 80)
            
            for test in tests:
                status_emoji = "✅" if test['passed'] else "❌"
                color = "green" if test['passed'] else "red"
                
                print(f"\n{status_emoji} {colorize(test['name'], fg=color)}")
                
                if test['doc']:
                    print(f"   📝 {test['doc']}")
                
                if test.get('setup_data'):
                    print("   🔧 Test Setup:")
                    if 'users' in test['setup_data']:
                        print(f"      • Created users:")
                        for role, user in test['setup_data']['users'].items():
                            if user:
                                print(f"        - {role}: {user['username']} ({user['email']})")
                    if 'user' in test['setup_data']:
                        print(f"      • Test user: {test['setup_data']['user']['username']}")
                    if 'challenge' in test['setup_data']:
                        ch = test['setup_data']['challenge']
                        print(f"      • Challenge: {ch['title']} ({ch['difficulty']}, {ch['points']} points)")
                    if 'solution' in test['setup_data']:
                        sol = test['setup_data']['solution']
                        print(f"      • Solution: {sol['language']} code: {sol['code']}")
                
                if test.get('test_data'):
                    print(f"   📤 Input Data: {test['test_data']}")
                
                if test.get('response'):
                    print("   📥 Response:")
                    if 'status' in test['response']:
                        print(f"      • Status: {test['response']['status']}")
                    if 'data' in test['response']:
                        print(f"      • Data: {test['response']['data']}")
                    if 'error' in test['response']:
                        print(f"      • Error: {test['response']['error']}")
                
                if test['error']:
                    print(f"   ❌ Error: {colorize(test['error'], fg='red')}")
            print()
        
        # Print summary
        print("=" * 80)
        print(colorize("📊 Summary", fg="cyan", opts=("bold",)))
        print("-" * 80)
        total = len(self.test_results)
        passed = sum(1 for t in self.test_results if t['passed'])
        failed = total - passed
        
        print(f"Total Tests: {colorize(str(total), fg='cyan')}")
        print(f"Passed: {colorize(str(passed), fg='green')}")
        print(f"Failed: {colorize(str(failed), fg='red')}")
        
        duration = time.time() - self.start_time
        print(f"\n⏱️  Duration: {colorize(f'{duration:.2f}s', fg='yellow')}")
        print("=" * 80 + "\n")

    def run_suite(self, suite, **kwargs):
        runner = self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            resultclass=self._get_custom_result_class()
        )
        return runner.run(suite)

    def _get_custom_result_class(self):
        runner = self  # Capture the runner instance
        
        class HumanReadableTestResult(TextTestResult):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.runner = runner

            def startTest(self, test):
                super().startTest(test)
                test_method = getattr(test, test._testMethodName)
                
                self.current_test = {
                    'name': test._testMethodName,
                    'module': test.__class__.__module__,
                    'doc': test_method.__doc__.strip() if test_method.__doc__ else None,
                    'setup_data': self.runner._get_readable_setup_data(test),
                    'test_data': getattr(test, 'test_data', None),
                    'response': None,
                    'passed': True,
                    'error': None
                }

            def addSuccess(self, test):
                super().addSuccess(test)
                if hasattr(test, 'current_test_response'):
                    self.current_test['response'] = self.runner._format_response(test.current_test_response)
                self.runner.test_results.append(self.current_test)

            def addError(self, test, err):
                super().addError(test, err)
                self._record_failure(test, err)

            def addFailure(self, test, err):
                super().addFailure(test, err)
                self._record_failure(test, err)

            def _record_failure(self, test, err):
                self.current_test.update({
                    'passed': False,
                    'error': self._exc_info_to_string(err, test)
                })
                self.runner.test_results.append(self.current_test)

        return HumanReadableTestResult 

    def _get_readable_setup_data(self, test):
        """Convert test setup data into human-readable format"""
        setup_data = {}
        
        # Get relevant attributes based on test class
        if hasattr(test, 'user1'):
            setup_data['users'] = {
                'follower': {
                    'username': test.user1.username,
                    'email': test.user1.email
                },
                'following': {
                    'username': test.user2.username,
                    'email': test.user2.email
                } if hasattr(test, 'user2') else None
            }
        
        if hasattr(test, 'user'):
            setup_data['user'] = {
                'username': test.user.username,
                'email': test.user.email
            }
        
        if hasattr(test, 'challenge'):
            setup_data['challenge'] = {
                'title': test.challenge.title,
                'difficulty': test.challenge.difficulty,
                'points': test.challenge.points
            }

        if hasattr(test, 'solution'):
            setup_data['solution'] = {
                'code': test.solution.code[:50] + '...' if len(test.solution.code) > 50 else test.solution.code,
                'language': test.solution.language
            }

        if hasattr(test, 'user_data'):
            setup_data['test_user'] = {
                'username': test.user_data['username'],
                'email': test.user_data['email']
            }

        return setup_data if setup_data else None

    def _format_response(self, response_data):
        """Format response data for readable output"""
        if not response_data:
            return None
        
        formatted = {}
        if 'status_code' in response_data:
            formatted['status'] = {
                201: 'Created Successfully',
                200: 'Success',
                400: 'Bad Request',
                401: 'Unauthorized',
                404: 'Not Found'
            }.get(response_data['status_code'], str(response_data['status_code']))
        
        if 'data' in response_data:
            formatted['data'] = response_data['data']
        if 'error' in response_data:
            formatted['error'] = response_data['error']
        
        return formatted 
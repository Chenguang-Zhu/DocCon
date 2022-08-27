#include <cstdlib>
#include <cstring>
#include <cctype>
#include <cstdio>
extern "C" {

  const char* lower(const char* x) {
	size_t len = strlen(x);
	char *lower_str = (char*) calloc(len+1, sizeof(char));
	for (size_t i = 0; i < len; ++i) {
	  lower_str[i] = tolower((unsigned char) x[i]);
	}
	return lower_str;
  }

  const int32_t beginWithUpper(const char* x) {
	if (isupper(x[0])) {
	  return 1;
	} else {
	  return 0;
	}
  }

  const char *testf() {
	return "ping from user-def functor";
  }

}


int main() {
  printf("%d", beginWithUpper("Abc"));
  printf("%d", beginWithUpper("abc"));
  printf("%d", beginWithUpper("aBC"));
}

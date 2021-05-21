# 다음 코드는 프로세스의 출력을 읽고, 프로세스가 오류 없이 깔끔하게 종료했는지 검사한다.
import subprocess

import os
os.environ['COMSPEC'] = 'powershell'

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    shell=True,
    encoding='utf-8')

result.check_returncode() # 예외가 발생하지 않으면 문제없이 잘 종료한 것 이다.
print(result.stdout)

# 파이썬에서 subprocess 등의 모듈을 통해 실행한 자식 프로세스는 부모 프로세스인 파이썬 인터프리터와 독립적으로 실행된다.
proc = subprocess.Popen(['sleep', '1'], shell=True)
while proc.poll() is None:
    print('작업 중 ...')
    # 시간이 걸리는 작업을 여기서 수행한다.
    import time
    time.sleep(0.3)

print('종료 상태', proc.poll())

# 자식 프로세스와 부모를 분리하면 부모 프로세스가 원하는 개수만큼 많은 자식 프로세스를 병렬로 실행할 수 있다.
import time

start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'], shell=True)
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()
end = time.time()
delta = end - start
print(f'{delta:.3f} 초 만에 끝남')


# 파이썬 프로그램의 데이터를 파이프를 사용해 하위 프로세스로 보내거나, 하위 프로세스의 출력을 받을 수 있다.
def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()  # 자식이 입력을 받도록 보장한다.
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)

# 암호화된 바이트 문자열을 출력한다.
for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])

# 다음 코드는 openssl 명령줄 도구를 하위 프로세스로 만들어서 입력 스트림의 월풀 해시를 계산한다.
def run_hash(input_stdin):
    return subprocess.Popen(
        ['openssl', 'dgst', '-whirlpool', '-binary'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    )

# 이제 데이터를 암호화하는 프로세스 집합을 실행하고, 이 프로세스들로부터 나온 암호화된 출력의 해시를 계산하는 프로세스 집합을 실행할 수 있다.
encrypt_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(100)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # 자식이 입력 스트림에 들어오는 데이터를 소비하고 communicate() 메서드가
    # 불필요하게 자식으로부터 오는 입력을 훔쳐가지 못하게 만든다.
    # 또 다운스트림 프로세스가 죽으면 SIGPIPE를 업스트림 프로세스에 전달한다.
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None

for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])

assert proc.returncode == 0

# 자식 프로세스가 멈추는 경우나 교착 상태를 방지하려면 timeout 파라미터를 사용하자
proc = subprocess.Popen(['sleep', '10'], shell=True)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('종료 상태', proc.poll())
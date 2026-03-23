#!/usr/bin/env python3

import time
import subprocess
import sys
import os


TEST_SERVER_CODE = '''import sys
sys.path.insert(0, 'src')

from wecom_app_svr.app import WecomAppServer


def message_handler(msg):
    class EchoMsg:
        def __init__(self, content):
            self.content = content

        def dump_xml(self):
            return f'<xml><Content>echo: {self.content}</Content></xml>'

    return EchoMsg(msg.content)


def event_handler(msg):
    class EventMsg:
        def __init__(self):
            self.content = 'event received'

        def dump_xml(self):
            return '<xml><Content>event received</Content></xml>'

    return EventMsg()


server = WecomAppServer(
    name="test_server",
    host="127.0.0.1",
    port=5000,
    path="/callback"
)

server.set_message_handler(message_handler)
server.set_event_handler(event_handler)

server_id = sys.argv[1] if len(sys.argv) > 1 else '1'
print(f"[Test Server {server_id}] Starting on 127.0.0.1:5000")

try:
    server.run()
except KeyboardInterrupt:
    print(f"\\n[Test Server {server_id}] Stopped")
'''


def run_process(cmd):
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def wait_startup(proc, timeout=3):
    time.sleep(timeout)
    return proc.poll() is None


def stop_process(proc, timeout=3):
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
        return True
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        return True


def test_quick_restart():
    print("\n" + "=" * 60)
    print("[测试 1] 快速重启测试")
    print("=" * 60)

    with open('test_server.py', 'w') as f:
        f.write(TEST_SERVER_CODE)

    print("\n步骤 1/3: 启动服务实例 1...")
    proc1 = run_process([sys.executable, 'test_server.py', '1'])

    if not wait_startup(proc1):
        print("✗ 服务实例 1 启动失败")
        return False
    print("✓ 服务实例 1 启动成功")

    print("\n步骤 2/3: 停止服务实例 1...")
    if not stop_process(proc1):
        print("✗ 停止服务实例 1 失败")
        return False
    print("✓ 服务实例 1 已停止")

    print("\n步骤 3/3: 立即启动服务实例 2（测试端口重用）...")
    time.sleep(0.5)
    proc2 = run_process([sys.executable, 'test_server.py', '2'])

    if not wait_startup(proc2):
        stdout, stderr = proc2.communicate()
        if "address already in use" in stderr.lower():
            print("✗ 端口被占用，端口重用功能失败")
            print(f"  错误: {stderr}")
            return False
        else:
            print("✗ 服务启动失败（非端口问题）")
            print(f"  错误: {stderr}")
            return False

    print("✓ 服务实例 2 启动成功！端口重用功能正常")
    stop_process(proc2)

    return True


def test_simultaneous_bind():
    print("\n" + "=" * 60)
    print("[测试 2] 同时绑定测试 (SO_REUSEPORT)")
    print("=" * 60)

    if not os.path.exists('test_server.py'):
        with open('test_server.py', 'w') as f:
            f.write(TEST_SERVER_CODE)

    print("\n步骤 1/2: 启动服务实例 A...")
    procA = run_process([sys.executable, 'test_server.py', 'A'])

    if not wait_startup(procA):
        print("✗ 服务实例 A 启动失败")
        return False
    print("✓ 服务实例 A 启动成功")

    print("\n步骤 2/2: 启动服务实例 B（测试同时绑定同一端口）...")
    procB = run_process([sys.executable, 'test_server.py', 'B'])

    if not wait_startup(procB):
        stdout, stderr = procB.communicate()
        if "address already in use" in stderr.lower():
            print("⚠ 不能同时绑定同一端口")
            print("  可能原因:")
            print("  - 系统不支持 SO_REUSEPORT（某些 Linux 内核版本）")
            print("  - 需要额外权限配置")
            print(f"  错误: {stderr}")
            stop_process(procA)
            return False
        else:
            print("✗ 服务启动失败（非端口问题）")
            print(f"  错误: {stderr}")
            stop_process(procA)
            return False

    print("✓ 服务实例 B 启动成功！SO_REUSEPORT 工作正常")

    stop_process(procA)
    stop_process(procB)

    return True


def cleanup():
    if os.path.exists('test_server.py'):
        os.remove('test_server.py')
    print("\n清理测试文件...")


def main():
    print("=" * 60)
    print("Flask 端口重用功能测试")
    print("=" * 60)
    print("测试环境: Linux")
    print(f"Python 版本: {sys.version.split()[0]}")

    results = {
        "快速重启": test_quick_restart(),
        "同时绑定": test_simultaneous_bind()
    }

    cleanup()

    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name}: {status}")

    print("\n" + "=" * 60)

    if all(results.values()):
        print("🎉 所有测试通过！端口重用功能工作正常")
        print("\n功能说明:")
        print("  - 快速重启: 服务停止后可以立即重启，无需等待端口释放")
        print("  - 同时绑定: 多个进程可以同时绑定同一端口（SO_REUSEPORT）")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查配置")
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        sys.exit(1)

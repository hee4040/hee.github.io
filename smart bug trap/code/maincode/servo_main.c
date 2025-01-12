#include <wiringPi.h>
#include <softPwm.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// GPIO 핀 번호 정의
#define SERVO_PIN1_1 0   // 유인제 분사용 서보모터1
#define SERVO_PIN1_2 24  // 유인제 분사용 서보모터2
#define SERVO_PIN2 6     // 문 닫기/열기용 서보모터
#define SERVO_PIN3_1 28  // 살충제 분사용 서보모터1
#define SERVO_PIN3_2 29  // 살충제 분사용 서보모터2

// 마지막으로 처리된 명령 저장
char lastCommand[256] = "";

// 서보모터의 각도를 설정하는 함수
void setServoAngle(int pin, int angle) {
    // 서보모터 각도에 따른 듀티 사이클 계산
    int dutyCycle = 5 + (angle * 20) / 180; // 0도=5, 180도=25
    printf("핀 %d, 각도 %d도, 듀티 사이클 %d\n", pin, angle, dutyCycle); // 디버깅 출력
    softPwmWrite(pin, dutyCycle); // 듀티 사이클 설정
    delay(500); // 0.5초 대기
}

// 서보모터를 초기화하거나 멈추는 함수
void resetServo(int pin) {
    setServoAngle(pin, 0); // 각도를 0도로 설정 (초기 위치)
    delay(500); // 동작 완료를 위해 대기
    softPwmWrite(pin, 0); // PWM 신호 중단
    printf("핀 %d 서보모터 정지\n", pin);
}

// 유인제 분사 함수
void sprayAttractant() {
    printf("유인제 분사\n");
    // 두 개의 유인제 분사용 서보모터를 작동
    setServoAngle(SERVO_PIN1_1, 90); // 90도로 이동
    setServoAngle(SERVO_PIN1_2, 90);
    delay(1000); // 1초 대기
    // 서보모터를 초기 위치로 복원
    resetServo(SERVO_PIN1_1);
    resetServo(SERVO_PIN1_2);
}

// 문 열기 함수
void openDoor() {
    printf("문 열기\n");
    setServoAngle(SERVO_PIN2, 0); // 0도로 이동 (문 열기)
    softPwmWrite(SERVO_PIN2, 0); // PWM 신호 중단
}

// 문 닫기 및 살충제 분사 함수
void closeDoorAndSprayPesticide() {
    printf("문 닫기\n");
    setServoAngle(SERVO_PIN2, 180); // 180도로 이동 (문 닫기)
    delay(3000); // 3초 대기
    softPwmWrite(SERVO_PIN2, 0); // PWM 신호 중단

    printf("살충제 분사\n");
    // 두 개의 살충제 분사용 서보모터를 작동
    setServoAngle(SERVO_PIN3_1, 90); // 90도로 이동
    setServoAngle(SERVO_PIN3_2, 90);
    delay(1000); // 1초 대기
    // 서보모터를 초기 위치로 복원
    resetServo(SERVO_PIN3_1);
    resetServo(SERVO_PIN3_2);
}

int main() {
    // WiringPi 초기화
    if (wiringPiSetup() == -1) {
        printf("WiringPi 초기화 실패!\n");
        return -1; // 오류 종료
    }

    // 서보모터 초기화 (PWM 생성)
    if (softPwmCreate(SERVO_PIN1_1, 0, 200) != 0 ||
        softPwmCreate(SERVO_PIN1_2, 0, 200) != 0 ||
        softPwmCreate(SERVO_PIN2, 0, 200) != 0 ||
        softPwmCreate(SERVO_PIN3_1, 0, 200) != 0 ||
        softPwmCreate(SERVO_PIN3_2, 0, 200) != 0) {
        printf("소프트웨어 PWM 초기화 실패!\n");
        return -1; // 오류 종료
    }

    printf("서보모터 제어 프로그램 시작\n");

    // 무한 반복 루프 (명령 대기)
    while (1) {
        FILE *file = fopen("/tmp/command.txt", "r"); // 명령 파일 열기
        if (file) {
            char command[256] = {0};
            // 파일에서 명령 읽기
            if (fscanf(file, "%s", command) == 1) {
                printf("명령 읽음: %s\n", command); // 디버깅 출력
                strcpy(lastCommand, command);

                // 유인제 분사 명령 처리
                if (strcmp(command, "spray_attractant") == 0) {
                    sprayAttractant();
                }
                // 문 닫기 및 살충제 분사 명령 처리
                else if (strcmp(command, "close_door_and_spray_pesticide") == 0) {
                    closeDoorAndSprayPesticide();
                    delay(3000); // 명령 처리 후 대기
                    openDoor(); // 문 열기
                }
            }
            fclose(file); // 파일 닫기
        }
        usleep(500000); // 0.5초 대기
    }

    return 0; // 프로그램 종료
}

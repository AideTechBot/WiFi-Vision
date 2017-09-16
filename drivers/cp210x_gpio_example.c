#include <iostream>
#include <fcntl.h>
#include <stropts.h>
#include <termios.h>

using namespace std;

int main()
{
	int fd;
	cout << "CP210x Serial Test\n";
	fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY);
	if (fd == -1)
	{
		cout << "Error opening port /dev/ttyUSB0\n";
		return -1;
	}

	unsigned long gpio;

	ioctl(fd, 0x8000, &gpio);
	cout << "original gpio = ";
	cout << hex << gpio << endl;
	gpio = ~gpio;
	gpio = gpio << 8;
	gpio |= 0x00FF;
	cout << "gpio = ";
	cout << hex << gpio << endl;
	ioctl(fd, 0x8001, &gpio);
	ioctl(fd, 0x8000, &gpio);
	cout << "new gpio = ";
	cout << hex << gpio << endl;

	close(fd);

	return 0;
}

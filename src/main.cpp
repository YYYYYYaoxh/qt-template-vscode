#include <QApplication>
#include <QLabel>

#if defined(HAVE_FMT)
#include <fmt/core.h>
#endif

int main(int argc, char **argv)
{
    QApplication app(argc, argv);

#if defined(HAVE_FMT)
    fmt::print("fmt is enabled via Conan: {}\n", "ok");
#endif

    QLabel label("Qt6 minimal template");
    label.resize(320, 120);
    label.show();

    return app.exec();
}

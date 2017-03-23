#include <sys/syscall.h>
#include <unistd.h>
#include <stdlib.h>

#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/scoped_ptr.hpp>
#include <boost/thread.hpp>
#include <iostream>
#include <vector>

#include "proto.h"

using boost::asio::ip::tcp;

pid_t gettid() {
    return syscall(SYS_gettid);
}

// A reference-counted non-modifiable buffer class.
class shared_const_buffer
{
    public:
        // Construct from a std::string.
        explicit shared_const_buffer(const std::string& data)
            : data_(new std::vector<char>(data.begin(), data.end())),
            buffer_(boost::asio::buffer(*data_))
    {
    }

        // Implement the ConstBufferSequence requirements.
        typedef boost::asio::const_buffer value_type;
        typedef const boost::asio::const_buffer* const_iterator;
        const boost::asio::const_buffer* begin() const { return &buffer_; }
        const boost::asio::const_buffer* end() const { return &buffer_ + 1; }

    private:
        boost::shared_ptr<std::vector<char> > data_;
        boost::asio::const_buffer buffer_;
};

class session
: public boost::enable_shared_from_this<session>
{
    public:
        session(boost::asio::io_service& io_service)
            : socket_(io_service)
           //  strand_(io_service)
        {
        }

        tcp::socket& socket()
        {
            return socket_;
        }

        void start()
        {
            // using namespace std; // For time_t, time and ctime.
            // time_t now = time(0);
            // shared_const_buffer buffer(ctime(&now));
            // boost::asio::async_write(socket_, buffer,
            //     boost::bind(&session::handle_write, shared_from_this()));
            boost::asio::mutable_buffers_1 buffer(valloc(sizeof(protohead)),sizeof(protohead));
            boost::asio::async_read(socket_,buffer,
                    boost::bind(&session::handle_read,
                        shared_from_this(),buffer,true,
                        boost::asio::placeholders::error));
        }

        void handle_write(boost::asio::mutable_buffers_1 &buffer)
        {
            //    std::cout << "tid " << gettid()  << std::endl;
            //    sleep(5);
            // free(boost::asio::buffer_cast<void*>(buffer));
            boost::asio::async_read(socket_,buffer,
                    boost::bind(&session::handle_read,
                        shared_from_this(),buffer,true,
                        boost::asio::placeholders::error));
        }

        void handle_read(boost::asio::mutable_buffers_1 &buffer,bool is_hdr,
                const boost::system::error_code &error) {
            if (error) {
                // read error
                return;
            }
            if (!is_hdr) {
                // response client
                char *buffer_data = boost::asio::buffer_cast<char*>(buffer);
                protohead *hdr = (protohead*)(buffer_data - sizeof(protohead));
                hdr->size = sizeof(*hdr);
                boost::asio::mutable_buffers_1 data_buffer(hdr,sizeof(*hdr));
                boost::asio::async_write(socket_,data_buffer,
                        boost::bind(&session::handle_write,shared_from_this(),data_buffer));
            } else {
                protohead *hdr = boost::asio::buffer_cast<protohead*>(buffer);
                char *new_buffer = (char*)realloc(hdr,hdr->size);
                char *data = new_buffer + sizeof(*hdr);
                size_t data_len = hdr->size - sizeof(*hdr);
                boost::asio::mutable_buffers_1 data_buffer(data,data_len);
                boost::asio::async_read(socket_,data_buffer,
                        boost::bind(&session::handle_read,shared_from_this(),
                                    data_buffer,false,
                                    boost::asio::placeholders::error));
            }
        }
    private:
        // The socket used to communicate with the client.
        tcp::socket socket_;
//        boost::asio::strand strand_;
};

typedef boost::shared_ptr<session> session_ptr;

class server
{
public:
    server(boost::asio::io_service& io_service, short port)
            : io_service_(io_service),
            acceptor_(io_service, tcp::endpoint(tcp::v4(), port))
            // strand_(io_service)
    {
        session_ptr new_session(new session(io_service_));
        acceptor_.async_accept(new_session->socket(),
               boost::bind(&server::handle_accept, this,
                       new_session,boost::asio::placeholders::error));
       // acceptor_.async_accept(new_session->socket(),
       //         strand_.wrap(boost::bind(&server::handle_accept, this,
       //                 new_session,boost::asio::placeholders::error)));
    }

    void handle_accept(session_ptr new_session,
            const boost::system::error_code& error)
    {
        std::cout << "new session tid " << gettid()  << std::endl;
        if (!error)
        {
            new_session->start();
        }

        new_session.reset(new session(io_service_));
        acceptor_.async_accept(new_session->socket(),
                boost::bind(&server::handle_accept, this,
                        new_session,boost::asio::placeholders::error));
        // acceptor_.async_accept(new_session->socket(),
        //         strand_.wrap(boost::bind(&server::handle_accept, this,
        //                 new_session,boost::asio::placeholders::error)));
    }

private:
    boost::asio::io_service& io_service_;
    tcp::acceptor acceptor_;
    // boost::asio::strand strand_;
};

typedef boost::thread* ThreadRef;

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: reference_counted <port>\n";
        return 1;
    }

    boost::asio::io_service io_service;

    using namespace std; // For atoi.
    server s(io_service, atoi(argv[1]));

    // std::vector<ThreadRef> thread_pool(5);
    // for (int i = 0; i < 5; ++i) {
    //     thread_pool.push_back(ThreadRef(new boost::thread(boost::bind(&boost::asio::io_service::run,&io_service))));
    // }
    io_service.run();

    // for (int i = 0; i < 5; ++i) {
    //     thread_pool[i]->join();
    // }
    return 0;
}

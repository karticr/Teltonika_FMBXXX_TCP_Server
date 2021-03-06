<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/karticr/Teltonika_FMBXXX_TCP_Server#getting-started">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Teltonika FMBXXX Tracker server</h3>

  <p align="center">
    Python based tcp server to recieve and control teltonika fmb devices
    <br />
    <a href="https://github.com/karticr/Teltonika_FMBXXX_TCP_Server#getting-started"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/issues">Report Bug</a>
    ·
    <a href="https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Teltonika FMBXXX server
This project is a basic server that gets data from the teltonica devices and prints them its a basic tcp server that can handle multiple clients. Documentation for building a ready made tcp server for controlling/ getting data out of the teltonica trackers was hard for me so i programmed this so that you could build your server off this.

Communication is based on documentation from the teltonika wiki <a href="https://wiki.teltonika-sas.com/wikibase/index.php?title=Teltonika_data_sending/receiving_protocols&mobileaction=toggle_view_mobile">teltonika tcp protocols</a>.


## Communicating with teltonika devices

once the tracker is setup with the server ip and port with tcp communication on the configurator. The tracker will open a connection to the server and send its IMEI.

<li>The first two bytes being the length of the IMEI number followed by the number. Once the server recieves the IMEI number it has to decide whether to accept the server by sending a reply or not.</li>

<li>01 to accept and 00 to reject.</li>

<li>this server is designed to accept all  incoming connections, but you can easily add in a  database of imei numbers to filter the connections.</li>

<li>after accepting the connection the tracker will start sending datapackets with information thats set on the i/o settings on the configurator, set the variables you want sent to atleast low, for the tracker to send it to the server.</li>
<li>after accepting this data the server must reply back to the server with the number of data received as a four byte integer otherwise the tracker will reset the connection this is done using the avlDecoder.py   its a class that parses the incoming data which is in codec 8 (<a href="https://wiki.teltonika-sas.com/wikibase/index.php?title=Teltonika_data_sending/receiving_protocols&mobileaction=toggle_view_mobile">teltonika tcp protocols</a>.) and returns a dictinary that has all the details along with the number of data the tracker sent</li>
<li>dict variable with the key ('no_record_i') has to be encoded into 4 byte integer and sent back to the server which is done on the main.py using the mResponse function</li>
<li>this server loops over to get the data from the trackers do what you want with the dict response</li>

## Getting started

<li>set the port you want to use on the main.py program</li>
<li>simply run the main.py </li>
<li>this will start the server and the server will print incoming data from the fmb devices periodically </li>

## Usage
I have also programed and compiled diffrent programs and datasets that can be useful for your application
<li>(<a href="https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/blob/main/avlIds.json">Avl Ids</a>) is a json list of all the avl varable ids and what they mean</li>
<li>(<a href="https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/blob/main/msgEncoder.py">msgEncode.py</a>) contains a class to encode messages into variouse differnt codecs that teltonica supports
    <ul>
        <li>msgToCodec12 is a function to convert messages into codec 12. codec 12 is used by the teltonica devices to accept sms/gprs commands</li>
        <li>controlling outputs, getting io information, etc</li>
        <li>all the available commands that the devices support are here <a href="https://wiki.teltonika-gps.com/view/Template:FMB_SMS/GPRS_Commands">msgEncode.py</a>
        </li>
        <li>inorder to encode the message simply call the  msgToCodec12 function with the gprs command </li>
        <li>and you can forward the return result from the above function to the tracker by using conn on main.py and  </li>
    </ul>
</li>
<li>AvlDecoder decodes incoming codec 8 messages from the tracker into a dict with 
    <ul>
        <li>codec id</li>
        <li>no of records (this has to be sent back to the tracker as an acknowledgement)</li>
        <li>crc-16 (crc-16/IBM)</li>
        <li>latitude, longitude, altitude, angle, no of satellites, speed</li>
        <li>io data (the input output 1 wire and other sensor information)</li>
    </ul>
</li>
<li>IO_decoder decodes the i/o information from the codec 18 message from the server</li>
<li>avlMatcher converts the avl ids into understandable variables using the avlIds.json</li>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/karticr/Teltonika_FMBXXX_TCP_Server?style=for-the-badge
[contributors-url]: https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/karticr/Teltonika_FMBXXX_TCP_Server?style=for-the-badge
[forks-url]: https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/network/members

[stars-shield]: https://img.shields.io/github/stars/karticr/Teltonika_FMBXXX_TCP_Server?style=for-the-badge
[stars-url]: https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/stargazers
[issues-shield]: https://img.shields.io/github/issues/karticr/Teltonika_FMBXXX_TCP_Server?style=for-the-badge
[issues-url]: https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/issues
[license-shield]: https://img.shields.io/github/license/karticr/Teltonika_FMBXXX_TCP_Server?style=for-the-badge
[license-url]: https://github.com/karticr/Teltonika_FMBXXX_TCP_Server/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-upwork-black.svg?style=for-the-badge&logo=upwork&colorB=555
[linkedin-url]: https://www.upwork.com/freelancers/~01d20139671a0c34bb
[product-screenshot]: images/screenshot.png
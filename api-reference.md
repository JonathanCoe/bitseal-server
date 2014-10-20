Bitseal Server API Reference
=======
<h2><span class="mw-headline" id="API_errors">API Commands</span></h2>
<p>Required arguments are denoted inside &lt; and &gt;  Optional arguments are inside [ and ]. 
</p>
<table class="wikitable">
<tr>
<th> Command </th>
<th> Parameters </th>
<th> On Success Returns </th>
<th> On Failure Returns </th>
<th> Description
</th></tr>
<tr>
<td> add </td>
<td> &lt;integer&gt; &lt;integer&gt; </td>
<td> An integer which is the sum of the two parameters </td>
<td> An API error </td>
<td> Returns the sum of the integers. Used as a simple test of the API.
</td></tr>
<tr>
<td> disseminateMsg </td>
<td> &lt;messageHex&gt; </td>
<td> 'Message disseminated successfully' </td>
<td> 'Message dissemination failed', or an API error </td>
<td> Takes a hex-encoded msg object and disseminates it to the rest of the Bitmessage network. The POW for the msg must have already been done.
</td></tr>
<tr>
<td> disseminatePubkey </td>
<td> &lt;pubkeyHex&gt; </td>
<td> 'Pubkey disseminated successfully' </td>
<td> 'Pubkey dissemination failed', or an API error  </td>
<td> Takes a hex-encoded pubkey object and disseminates it to the rest of the Bitmessage network. The POW for the pubkey must have already been done.
</td></tr>
<tr>
<td> disseminateGetpubkey </td>
<td> &lt;getpubkeyHex&gt; </td>
<td> 'Getpubkey disseminated successfully' </td>
<td> 'Getpubkey dissemination failed', or an API error  </td>
<td> Takes a hex-encoded getpubkey object and disseminates it to the rest of the Bitmessage network. The POW for the getpubkey must have already been done.
</td></tr>
<tr>
<td> requestPubkey </td>
<td> &lt;identifierHex&gt; &lt;addressVersion&gt; </td>
<td> The hex-encoded pubkey object, formatted as a single object in a JSON array </td>
<td> 'No pubkeys found', or an API error  </td>
<td> Takes an 'identifer' value and address version number and attempts to find a matching pubkey in the server's storage. The identifier value is ripe hash or the 'tag' of the pubkey which is being requested, depending on the address version of the pubkey. If a matching pubkey is found, it is returned to the client.
</td></tr>
<tr>
<td> checkForNewMsgs </td>
<td> &lt;streamNumber&gt; &lt;receivedSinceTime&gt; &lt;receivedBeforeTime&gt; </td>
<td> A JSON array containing the hex-encoded msg objects </td>
<td> 'No msgs found', or an API error  </td>
<td> Takes a stream number, a 'received since' time value, and a 'received before' time value and returns any msg objects which were received in that stream number at a time between the two provided values.
</td></tr>
</table>
<p><br />
</p>
<h2><span class="mw-headline" id="API_errors">API errors</span></h2>
<p>Here are the various error codes and messages you might see. Parts of the error messages in BLOCK_CAPITALS are variable fields that will change based on the data involved in the error.
</p>
<table class="wikitable">
<tr>
<th> Error Number</th>
<th> Message
</th></tr>
<tr>
<td> 000 </td>
<td> API Error 000: 'I need NUMBER_OF_PARAMETERS parameters!'
</td></tr>
<tr>
<td> 001 </td>
<td> API Error 001: 'Decode error - DECODE_EXCEPTION_MESSAGE. Had trouble while decoding string: YOUR_STRING'
</td></tr>
<tr>
<td> 002 </td>
<td> API Error 002: 'The address version cannot be less than ADDRESS_VERSION_NUMBER'
</td></tr>
<tr>
<td> 003 </td>
<td> API Error 003: 'Address versions above ADDRESS_VERSION_NUMBER are currently not supported'
</td></tr>
<tr>
<td> 004 </td>
<td> API Error 004: 'The length of hash should be 20 bytes (encoded in hex and thus 40 characters).'
</td></tr>
<tr>
<td> 005 </td>
<td> API Error 005: 'The length of tag should be 32 bytes (encoded in hex and thus 64 characters).'
</td></tr>
<tr>
<td> 006 </td>
<td> API Error 006: 'The requested object was found, but its payload is above the maximum size limit. The size of the object payload is PAYLOAD_SIZE_IN_BYTES'
</td></tr>
</table>

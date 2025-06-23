<?php
// app/Events/MessageUpdated.php
namespace App\Events;

use App\Models\Message;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class MessageUpdated implements ShouldBroadcast
{
    use SerializesModels;

    public function __construct(public Message $message) {}

    public function broadcastOn(): Channel
    {
        // canale privato per la conversazione
        return new PrivateChannel('conversations.'.$this->message->conversation_id);
    }

    public function broadcastWith(): array
    {
        return [
            'id'      => $this->message->id,
            'content' => $this->message->content,
            'sender'  => $this->message->sender,
        ];
    }
}

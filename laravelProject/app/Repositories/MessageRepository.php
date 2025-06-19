<?php
namespace App\Repositories;

use App\Models\Conversation;          // ⬅️ importa
use App\Models\Message;
use App\Repositories\Contracts\MessageRepositoryInterface;
use App\Utils\OaRepository;

class MessageRepository implements MessageRepositoryInterface
{
    public function store(Conversation $conversation, array $data): Message
    {
        $newMessage = new Message();

        // foreign-keys
        $newMessage->conversation_id = $conversation->id;
        $newMessage->user_id         = OaRepository::store($data, 'user_id') ?: 1;

        // payload veri e propri
        $newMessage->sender  = OaRepository::store($data, 'sender');
        $newMessage->content = OaRepository::store($data, 'content');

        $newMessage->save();

        return $newMessage;
    }

    public function update(int $messageId, array $data): Message
    {
        $dbMessage = Message::findOrFail($messageId);

        $dbMessage->content = OaRepository::update($data, 'content', $dbMessage);
        $dbMessage->sender  = OaRepository::update($data, 'sender',  $dbMessage);
        // In genere non cambi conversation_id / user_id su update,
        // ma se davvero ti serve lasciali pure
        $dbMessage->save();

        return $dbMessage;
    }
}

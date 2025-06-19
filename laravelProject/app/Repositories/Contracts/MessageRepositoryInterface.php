<?php


namespace App\Repositories\Contracts;


use App\Models\Conversation;
use App\Models\Message;

interface MessageRepositoryInterface
{
    public function store(Conversation $conversation, array $data): Message;
    public function update(int $messageId, array $data): Message;
}


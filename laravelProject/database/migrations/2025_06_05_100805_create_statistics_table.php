<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('statistics', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('document_id');
            $table->text('model_llm');
            $table->text('model_embedding');
            $table->integer('token_prompt')->nullable();
            $table->integer('token_response')->nullable();
            $table->integer('token_used')->nullable();
            $table->text('prompt');
            $table->integer('model_max_tokens');
            $table->float('model_temperature');
            $table->text('model_llm_api');
            $table->text('model_embedding_api');
            $table->integer('chunk_size');
            $table->integer('chunk_overlap');
            $table->integer('number_response_llm')->nullable();
            $table->timestamps();
            $table->foreign('document_id')->references('id')->on('documents')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('statistics');
    }
};

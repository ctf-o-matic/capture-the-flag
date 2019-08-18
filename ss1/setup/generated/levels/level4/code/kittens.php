<?php 

$comments = array('Kitty-kitty-kitty', 'The most adorable', 'meow', 'purrrrrr...', 'How cute is this kitten?', '🥺', 'So cute');

if(!isset($_GET['index'])) {
    $index = 1;
} else {
    $index = $_GET['index'];
}

if ($index > 0 && $index <= 16) {
    if(!is_numeric($index)) {
  
        $logMsg = "Unauthorized value $index. Index should be a number";
        file_put_contents("wwwdata/errors.log", $logMsg);
        die("Kitty-kitty-kitty... Where are you ?");
    } else {
        echo "<body style='text-align: center'>";
        echo "<img src='http://placekitten.com/500/500?image=$index'>";
        echo "<footer style='font-size: x-large' >";
        if($index > 1) {
            $previousIndex = $index-1;
            echo "<a href='index.php?app=kittens.php&index=$previousIndex'>&#8592;</a>";
        }
        $comment = $comments[array_rand($comments)];
        echo "<span>| $comment |</span>";
        if($index < 16) {
            $nextIndex = $index+1;
            echo "<a href='index.php?app=kittens.php&index=$nextIndex'>&#8594;</a>";
        }
        echo "</footer>";
        echo "</body>";
    }

} else {

    $logMsg = "Unauthorized value. Index must be in range 1-16";
    file_put_contents("wwwdata/errors.log", $logMsg);
}

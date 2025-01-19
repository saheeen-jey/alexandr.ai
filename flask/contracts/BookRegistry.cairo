%lang starknet

@storage_var
func book_count() -> (count: felt) {
}

@storage_var
func book_title(book_id: felt) -> (title: felt) {
}

@storage_var
func book_cid_part1(book_id: felt) -> (cid_p1: felt) {
}

@storage_var
func book_cid_part2(book_id: felt) -> (cid_p2: felt) {
}

/**
  A simple event to notify whenever a new book is stored
*/
@event
func BookStored(book_id: felt, title: felt) {
}

/**
  Increments book_count and stores the title + IPFS CID (split into two felts).
  
  title        - a short title stored as a single felt
  cid_part1    - first part of your IPFS CID if needed
  cid_part2    - second part of your IPFS CID if needed
*/
@external
func store_book(title: felt, cid_part1: felt, cid_part2: felt) {
    alloc_locals;
    let (current_count) = book_count.read();
    let new_count = current_count + 1;

    book_count.write(new_count);
    book_title.write(new_count, title);
    book_cid_part1.write(new_count, cid_part1);
    book_cid_part2.write(new_count, cid_part2);

    BookStored(new_count, title);
    return ();
}

/**
  Retrieves stored book information by ID.
*/
@view
func get_book(book_id: felt) -> (
    title: felt, 
    cid_part1: felt, 
    cid_part2: felt
) {
    let (title) = book_title.read(book_id);
    let (cid_p1) = book_cid_part1.read(book_id);
    let (cid_p2) = book_cid_part2.read(book_id);
    return (title, cid_p1, cid_p2);
}

/**
  Returns the current number of books stored in the contract.
*/
@view
func get_book_count() -> (count: felt) {
    let (count) = book_count.read();
    return (count,);
}

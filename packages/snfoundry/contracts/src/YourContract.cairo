#[starknet::interface]
trait ITitleToIPFSContract<T> {
    fn get(self: @T, title: felt252) -> ByteArray;
    fn addBook(ref self: T, title: felt252, ipfs_id: ByteArray);
}

#[starknet::contract]
mod YourContract {
    use starknet::storage::{
        StoragePointerReadAccess, StoragePointerWriteAccess, StoragePathEntry, Map,
    };

    #[storage]
    struct Storage {
        myMap: Map::<felt252, ByteArray>
    }

    #[constructor]
    fn constructor(ref self: ContractState) {
        self.myMap.entry('joe biden').write("joe biden");
    }

    #[abi(embed_v0)]
    impl TitleToIPFSContract of super::ITitleToIPFSContract<ContractState> {
        fn get(self: @ContractState, title: felt252) -> ByteArray {
            self.myMap.entry(title).read()
        }

        fn addBook(ref self: ContractState, title: felt252, ipfs_id: ByteArray) {
            self.myMap.entry(title).write(ipfs_id);
        }
    }
}
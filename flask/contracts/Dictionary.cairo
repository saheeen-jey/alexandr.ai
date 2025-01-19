#[starknet::interface]
trait ITitleToIPFSContract<T> 
{
    fn get(self: @T, title: felt252) -> ByteArray;
    fn addBook(ref self: T, title: felt252, ipfs_id: ByteArray);
}

#[starknet::contract]
mod Book2TitleToIPFSContract {
    use starknet::ContractAddress;
    use starknet::storage::{Map, StorageMapReadAccess, StorageMapWriteAccess};
    use traits::Into;

    #[storage]
    struct Storage {
        myMap: Map::<u256, ByteArray>
    }

    #[constructor]
    fn constructor(ref self: ContractState) {
        self.myMap.write('joe biden', "joe biden")
    }

    #[abi(embed_v0)]
    impl TitleToIPFSContract of super::ITitleToIPFSContract<ContractState> 
    {
        fn get(self: @ContractState, title: felt252) -> ByteArray {
            self.myMap.entry(title).read()
        }
        fn addBook(ref self: ContractState, title: felt252, ipfs_id: ByteArray) {
            self.myMap.entry(title).write(ipfs_id)
        }
    }
}
import { PinataSDK } from "pinata-web3";

const pinata = new PinataSDK({
  pinataJwt: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlY2RjN2FhZS00MTI4LTQyZTAtODE1Yi0xMzZhNDczZmZiMGQiLCJlbWFpbCI6InNoYXZvbi50aGFkYW5pQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI2ZjRjYjQxY2Y0MTY2MzgzOGZkNiIsInNjb3BlZEtleVNlY3JldCI6ImRhMDZhYThjMmMyNTg4NDZhY2NmNjk0NzMwZWJlNzIwNjM5ZGNjNjk0MDNmYjE1YjM3MWFjMWRiYTNmZmMzMjkiLCJleHAiOjE3Njg3NDIzMzl9.WXPFvzT5j0W7MtSvQy7kw8NcgB4fuafB81VdKJ3wmyY",
  pinataGateway: "https://gateway.pinata.cloud",
});
async function main() {
    try {
      const file = new File(["hello"], "Testing.txt", { type: "text/plain" });
      const upload = await pinata.upload.file(file);
      console.log(upload);
    } catch (error) {
      console.log(error);
    }
  }
  
  await main();